import asyncio
import websockets

from src.common.interfaces import ElevatorStatus
from src.common.models import Elevator, ElevatorDirection
from src.common.utils import get_open_port, get_settings, get_ws_uri


__all__ = ["run_elevator"]


class ElevatorProcess:
    """Elevator class to handle tracking instance variables and the websocket connection"""

    def __init__(
        self,
        ws: websockets.WebSocketClientProtocol,
        host: str,
        port: int,
        min_status_wait: float,
    ):
        self.ws = ws  # websocket connection
        self.min_status_wait: float = min_status_wait  # number of seconds to wait between sending statuses
        self._elevator: Elevator = Elevator(host=host, port=port)

    async def send_status(self):
        """Send status message for this elevator"""
        msg_bytes: bytes = ElevatorStatus.serialize(self._elevator)
        print(f"Sending status {msg_bytes}")
        await self.ws.send(msg_bytes)

    async def receive_instruction(self) -> bool:
        """Wait to receive an instruction"""
        try:
            raw_data: bytes = await asyncio.wait_for(
                self.ws.recv(), timeout=self.min_status_wait
            )
            data: str = raw_data.decode("utf8")

            return True
        except asyncio.TimeoutError:
            return False

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

    async def simulate_move(self, direction: ElevatorDirection):
        """Simulate an elevator moving between floors by waiting and then
        changing the floor value"""
        await asyncio.sleep(2.0)
        self._elevator.floor += direction.value

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
        ev = cls(
            ws=ws,
            host=config.ELEVATOR_HOST,
            port=get_open_port(),
            min_status_wait=config.MIN_STATUS_WAIT,
        )
        # run the instance
        await ev.run()


def run_elevator():
    asyncio.run(ElevatorProcess.create_and_run())
