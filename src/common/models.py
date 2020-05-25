import json
import random
from typing import Dict


class ElevatorController:
    """Track a group of elevators"""

    # host/port mapping to Elevator class
    elevators: Dict[str, "Elevator"] = dict()

    @classmethod
    def receive_elevator_status(cls, raw_data: bytes):
        """Update data about an elevator based in incoming data"""
        data_dict: dict = json.loads(raw_data.decode("utf8"))
        host = data_dict["host"]
        port = data_dict["port"]
        host_and_port = f"{host}:{port}"
        if host_and_port not in cls.elevators:
            cls.elevators[host_and_port] = Elevator(host=host, port=port)
        print(f"Elevators: {cls.elevators}")

    @classmethod
    def as_dict(cls) -> dict:
        """Serialize the controller's status to a dict"""
        status: dict = {}
        for i in range(3):
            status[i] = Elevator(
                host="cool.org",
                port=random.randint(8000, 9000),
                floor=random.randint(0, 10),
            ).as_dict()
        return status


class Elevator:
    """Track data about an Elevator"""

    def __init__(self, host, port, floor=None):
        self.host = host
        self.port = port
        self.floor = floor

    def as_dict(self) -> dict:
        """Serialize to a dictionary"""
        return {"host": self.host, "port": self.port, "floor": self.floor}
