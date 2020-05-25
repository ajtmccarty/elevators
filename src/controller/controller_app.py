import json

from sanic import Sanic, Blueprint
from sanic.response import empty
from sanic.websocket import WebSocketProtocol

from src.common.utils import get_settings


__all__ = ["app", "run_controller"]

ev_ctl_web_bp = Blueprint("ElevatorWebController")
elevators = []


@ev_ctl_web_bp.route("/button/<floor>/<direction>")
async def button(request, floor, direction):
    print(f"Received: floor: {floor}, direction: {direction}")
    return empty()


@ev_ctl_web_bp.websocket("/elevator")
async def elevator_connection(request, ws):
    try:
        while True:
            await receive_elevator_status(ws)
    except BaseException:
        await ws.close()
        raise


async def receive_elevator_status(ws):
    global elevators
    print("Waiting to receive", end="...")
    raw_data: bytes = await ws.recv()
    data_dict: dict = json.loads(raw_data.decode("utf8"))
    print(f"Received {data_dict!r}")
    host = data_dict["host"]
    port = data_dict["port"]
    host_and_port = f"{host}:{port}"
    if host_and_port not in elevators:
        elevators.append(host_and_port)
    print(f"Elevators: {elevators}")


def get_controller_app() -> Sanic:
    """Get the Sanic app for the controller"""
    the_app = Sanic("ElevatorCtl")
    the_app.config = get_settings()
    the_app.blueprint(ev_ctl_web_bp)
    return the_app


app = get_controller_app()


def run_controller():
    """Run the Sanic app with config options from the files"""
    app.run(
        host=app.config.CONTROLLER_HOST,
        port=app.config.CONTROLLER_PORT,
        debug=app.config.DEBUG,
        protocol=WebSocketProtocol,
    )
