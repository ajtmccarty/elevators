"""Functions for managing setting/getting elevator state on Redis"""
import aredis

from src.elevators.instance import get_elevator_instance_app

__all__ = [
    "get_elevator_floor",
    "pop_from_elevator_queue",
    "push_to_elevator_queue",
    "set_elevator_floor"
]


class RedisClient:

    _client = None

    @classmethod
    def __new__(cls, *args, **kwargs) -> aredis.StrictRedis:
        if not cls._client:
            cls._client = cls.__get_redis_client(*args, **kwargs)
        return cls._client

    @staticmethod
    def __get_redis_client(*args, **kwargs) -> aredis.StrictRedis:
        app = get_elevator_instance_app()
        redis_settings: dict = app.config.REDIS
        client = aredis.StrictRedis(
            host=redis_settings["HOST"],
            port=redis_settings["PORT"],
            password=redis_settings.get("PASSWORD"),
            username=redis_settings.get("USERNAME"),
        )
        return client

#####################
# FLOOR GET AND SET #
#####################


def get_ev_floor_key(elevator_id: int) -> str:
    return f"ev_floor_{elevator_id}"


async def get_elevator_floor(ev_id: int) -> str:
    client = RedisClient()
    ev_key = get_ev_floor_key(ev_id)
    return await client.get(ev_key).decode()


async def set_elevator_floor(ev_id: int, floor: int) -> str:
    client = RedisClient()
    ev_key = get_ev_floor_key(ev_id)
    return await client.set(ev_key, floor).decode()

######################
# QUEUE PUSH AND POP #
######################


def get_ev_queue_key(elevator_id: int) -> str:
    return f"ev_queue_{elevator_id}"


async def pop_from_elevator_queue(ev_id: int, floor: int):
    client = RedisClient()
    ev_key = get_ev_queue_key(ev_id)
    return await client.lpop(ev_key, floor)


async def push_to_elevator_queue(ev_id: int, floor: int):
    client = RedisClient()
    ev_key = get_ev_queue_key(ev_id)
    return await client.rpush(ev_key, floor)