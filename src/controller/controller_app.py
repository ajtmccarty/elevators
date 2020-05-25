import asyncio

from sanic import Sanic, Blueprint
from sanic.response import empty, html
from sanic.websocket import WebSocketProtocol

from src.common.utils import get_settings, get_ws_uri
from src.common.models import ElevatorController
from src.controller.html_templates import CONTROLLER_STATUS_HTML


__all__ = ["app", "run_controller"]


async def button(request, floor, direction):
    print(f"Received: floor: {floor}, direction: {direction}")
    return empty()


async def ctl_status_view(request):
    """Very simple HTML page for getting realtime update on controller status"""
    the_app: Sanic = request.app
    uri = get_ws_uri(
        host=the_app.config.CONTROLLER_HOST,
        port=the_app.config.CONTROLLER_PORT,
        path=the_app.url_for("ctl_status_ws"),
    )
    html_data: str = CONTROLLER_STATUS_HTML.format(uri=uri)
    return html(html_data)


async def handle_status_ws(request, ws):
    """Send the Elevator Controller's status over the ctl websocket"""
    while True:
        print("Sending", end="...")
        data: dict = ElevatorController.as_dict()
        # send the __repr__ of the data
        await ws.send(f"{data!r}")
        print(f"{data!r}")
        await asyncio.sleep(3.0)


async def handle_elevator_ws(request, ws):
    """Send incoming Elevator status data to the Elevator Controller"""
    try:
        while True:
            print("Waiting to receive", end="...")
            raw_data: bytes = await ws.recv()
            print(f"Received {raw_data!r}")
            ElevatorController.receive_elevator_status(raw_data)

    except BaseException:
        await ws.close()
        raise


def build_ctl_bp() -> Blueprint:
    """Build an Elevator Controller BP"""
    ev_ctl_bp = Blueprint("ev_ctl")
    ev_ctl_bp.add_websocket_route(handle_elevator_ws, "/elevator", name="elevator_ws")
    ev_ctl_bp.add_websocket_route(handle_status_ws, "/status/ws", name="ctl_status_ws")
    ev_ctl_bp.add_route(ctl_status_view, "/status", name="ctl_status")
    ev_ctl_bp.add_route(button, "/button/<floor>/<direction>", name="button")
    return ev_ctl_bp


def get_controller_app() -> Sanic:
    """Get the Sanic app for the controller"""
    the_app = Sanic("ElevatorCtl")
    the_app.config = get_settings()
    ev_ctl_bp = build_ctl_bp()
    the_app.blueprint(ev_ctl_bp)
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
