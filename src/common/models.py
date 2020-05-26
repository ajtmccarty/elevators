from enum import Enum
from typing import Dict

from src.common.interfaces import Message


class ElevatorDirection(Enum):
    UP = 1
    DOWN = -1


class ElevatorController:
    """Track a group of elevators"""

    # host/port mapping to Elevator class
    elevators: Dict[str, "Elevator"] = dict()

    @classmethod
    def receive_elevator_status(cls, raw_data: bytes):
        """Update data about an elevator based in incoming data"""
        ev = Message.deserialize(raw_data)
        host_port: str = ev.host_and_port
        if host_port not in cls.elevators:
            cls.elevators[host_port] = ev
        print(f"Elevators: {cls.elevators}")

    @classmethod
    def as_dict(cls) -> dict:
        """Serialize the controller's status to a dict"""
        return {k: v.as_dict() for k, v in cls.elevators.items()}


class Elevator:
    """Track data about an Elevator"""

    def __init__(self, host, port, floor=None):
        self.host = host
        self.port = port
        self.floor = floor

    @classmethod
    def from_dict(cls, data_dict: dict) -> "Elevator":
        """Create an Elevator from a serialized dict"""
        return cls(**data_dict)

    def as_dict(self) -> dict:
        """Serialize to a dictionary"""
        return {"host": self.host, "port": self.port, "floor": self.floor}

    @property
    def host_and_port(self):
        return f"{self.host}:{self.port}"

    def add_dest(self, floor: int):
        pass
