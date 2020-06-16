from enum import Enum
from typing import Dict, Optional

from src.common.interfaces import ElevatorAddFloor, ElevatorStatus, Message


class ElevatorDirection(Enum):
    UP = 1
    DOWN = -1


class ElevatorController:
    """Track a group of elevators"""

    # host/port mapping to Elevator class
    elevators: Dict[str, "Elevator"] = dict()

    @classmethod
    def get_ev(cls, host_and_port: str) -> Optional["Elevator"]:
        return cls.elevators.get(host_and_port)

    @classmethod
    def receive_elevator_msg(cls, raw_data: bytes):
        """Update data about an elevator based in incoming data"""
        msg: Message = Message.deserialize_raw(raw_data)
        if isinstance(msg, ElevatorStatus):
            cls.handle_status_msg(msg)
        if isinstance(msg, ElevatorAddFloor):
            cls.handle_add_floor(msg)

    @classmethod
    def handle_status_msg(cls, msg: ElevatorStatus):
        host_port: str = msg.elevator.host_and_port
        if host_port not in cls.elevators:
            cls.elevators[host_port] = msg.elevator
        print(f"Elevators: {cls.elevators}")

    @classmethod
    def handle_add_floor(cls, msg: ElevatorAddFloor):
        instr = msg.instruction
        instr.execute()

    @classmethod
    def as_dict(cls) -> dict:
        """Serialize the controller's status to a dict"""
        return {k: v.as_dict() for k, v in cls.elevators.items()}


class Elevator:
    """Track data about an Elevator"""

    def __init__(self, host, port, floor=None, queue=None):
        self.host = host
        self.port = port
        self.floor = floor
        # list to track next destinations
        self._queue = queue or []

    @classmethod
    def from_dict(cls, data_dict: dict) -> "Elevator":
        """Create an Elevator from a serialized dict"""
        return cls(**data_dict)

    def as_dict(self) -> dict:
        """Serialize to a dictionary"""
        return {
            "host": self.host,
            "port": self.port,
            "floor": self.floor,
            "queue": self._queue,
        }

    @property
    def host_and_port(self) -> str:
        return f"{self.host}:{self.port}"

    def add_dest(self, floor: int) -> None:
        self._queue.append(floor)


class ElevatorInstruction:
    def __init__(self, host_and_port: str, elevator: Elevator):
        self.host_and_port: str = host_and_port
        self.elevator: Elevator = elevator

    def execute(self):
        return NotImplemented

    @classmethod
    def from_dict(cls, data_dict: dict) -> "ElevatorInstruction":
        host_and_port = data_dict.get("host_and_port")
        ev: Elevator = ElevatorController.get_ev(host_and_port=host_and_port)
        return cls(**data_dict, elevator=ev)

    def as_dict(self) -> dict:
        return {
            "host_and_port": self.host_and_port,
        }


class AddFloorToQueue(ElevatorInstruction):
    def __init__(self, *args, floor: int, **kwargs):
        super().__init__(*args, **kwargs)
        self.floor: int = floor

    def execute(self):
        self.elevator.add_dest(self.floor)

    def as_dict(self) -> dict:
        data_dict: dict = super().as_dict()
        data_dict["floor"] = self.floor
        return data_dict
