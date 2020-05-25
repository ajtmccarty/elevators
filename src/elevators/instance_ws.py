import asyncio
import json
import time
import websockets

from src.common.utils import get_open_port, get_settings, get_ws_uri


__all__ = ["run_elevator"]


class Elevator:
    """Elevator class to handle tracking instance variables and the websocket connection"""

    # number of seconds to wait before sending status
    status_min_wait: int = 3

    def __init__(self, ws: websockets.WebSocketClientProtocol, host: str, port: int):
        self.ws = ws  # websocket connection
        self.host = host
        self.port = port
        self.floor = None  # initial floor
        self.last_status = 0

    def as_dict(self) -> dict:
        """Serialize the instance as a dictionary"""
        return dict(host=self.host, port=self.port, floor=self.floor)

    async def send_status(self):
        """Send status message roughly every status_min_wait settings"""
        if time.time() - self.last_status > self.status_min_wait:
            msg_dict: dict = self.as_dict()
            msg_bytes = json.dumps(msg_dict).encode("utf-8")
            print(f"Sending status {msg_dict!r}")
            await self.ws.send(msg_bytes)
            self.last_status = time.time()

    async def receive_instruction(self):
        raw_data = await self.ws.recv()
        # TODO: handle instruction

    async def run(self):
        """Handle sending and receiving over the websocket until stopped"""
        try:
            while True:
                await self.send_status()
                await self.receive_instruction()
        # BaseException instead of Exception here to catch KeyboardInterrupt
        except BaseException:
            await self.ws.close()
            raise

    @classmethod
    async def create_and_run(cls):
        """Factory method for creating an elevator instance"""
        config = get_settings()
        # build the websocket URI from the config CONTROLLER_HOST and _PORT
        ws_uri = get_ws_uri(
            host=config.CONTROLLER_HOST, port=config.CONTROLLER_PORT, path="elevator"
        )
        # make the connection
        ws = await websockets.connect(ws_uri)
        # make the instance
        ev = cls(ws=ws, host=config.ELEVATOR_HOST, port=get_open_port())
        # run the instance
        await ev.run()


def run_elevator():
    asyncio.run(Elevator.create_and_run())
