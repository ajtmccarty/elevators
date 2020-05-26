import json
from typing import Any, Dict, Union


class Message:

    msg_types: Dict[str, "Message"] = {}
    msg_type = None

    @classmethod
    def register_msg_type(cls, subclass):
        """Map msg_type to Message subclasses for use in deserialization"""
        assert isinstance(subclass, cls)
        cls.msg_types[subclass.msg_type] = subclass

    @classmethod
    def serialize(cls, the_object: Any) -> Union[bytes, str]:
        """Serialize a Message to bytes or a str

        Very simple method right now, but
        """
        assert cls.msg_type
        assert hasattr(the_object, "as_dict")
        obj_data: dict = the_object.as_dict()
        full_msg: dict = {"payload": obj_data, "msg_type": cls.msg_type}
        return json.dumps(full_msg).encode("utf8")

    @classmethod
    def deserialize(cls, raw_data: bytes) -> Any:
        msg_dict: dict = json.loads(raw_data.decode("utf8"))
        assert "payload" in msg_dict
        assert "msg_type" in msg_dict
        msg_type_class = cls.msg_types[msg_dict["msg_type"]]
        return msg_type_class.deserialize(msg_dict["payload"])


class ElevatorStatus(Message):
    """Message for (de)serializing an elevator's status"""

    msg_type = "ev_status"

    @classmethod
    def deserialize(cls, payload: dict) -> "Elevator":
        from src.common.models import Elevator

        return Elevator.from_dict(payload)


Message.register_msg_type(ElevatorStatus())
