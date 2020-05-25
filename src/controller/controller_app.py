import json

from sanic import Sanic, Blueprint
from sanic.response import empty, html
from sanic.websocket import WebSocketProtocol

from src.common.utils import get_settings, get_ws_uri
from src.controller.html_templates import CONTROLLER_STATUS_HTML


__all__ = ["app", "run_controller"]

ev_ctl_web_bp = Blueprint("ev_ctl")
elevators = []


@ev_ctl_web_bp.route("/button/<floor>/<direction>")
async def button(request, floor, direction):
    print(f"Received: floor: {floor}, direction: {direction}")
    return empty()


@ev_ctl_web_bp.websocket("/status/ws", name="ctl_status_ws")
async def ctl_status_ws(request, ws):
    """Web sockets route for updating controller status"""
    await ws.send("Status")


@ev_ctl_web_bp.route("/status")
async def ctl_status_view(request):
    """Very simple HTML page for getting realtime update on controller status"""
    the_app: Sanic = request.app
    uri = get_ws_uri(
        host=the_app.config.CONTROLLER_HOST,
        port=the_app.config.CONTROLLER_PORT,
        path=the_app.url_for("ctl_status_ws")
    )
    html_data: str = CONTROLLER_STATUS_HTML.format(
        uri=uri
    )
    return html(html_data)


@ev_ctl_web_bp.websocket("/elevator", name="elevator_ws")
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
