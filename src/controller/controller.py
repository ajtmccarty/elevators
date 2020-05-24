import os
from pathlib import Path

from sanic import Sanic, Blueprint
from sanic.response import json
from sanic.websocket import WebSocketProtocol
import websockets

__all__ = ["get_controller_app"]

conf_env_var_name = "ELEVATOR_SETTINGS"
ev_ctl_web_bp = Blueprint("ElevatorWebController")


@ev_ctl_web_bp.route("/button/<floor>/<direction>")
async def button(request, floor, direction):
    print(f"Received: floor: {floor}, direction: {direction}")
    host = request.app.config.ELEVATOR_HOST
    port = request.app.config.ELEVATOR_PORT
    uri = f"ws://{host}:{port}/instruction/"
    msg = f"{floor}, {direction}"
    async with websockets.connect(uri) as ws:
        print(f"Sending {msg!r}")
        await ws.send(msg)
        print(f"Waiting on response", end="...")
        resp = await ws.recv()
        print(f"{resp!r}")

    return json({
        "floor": floor,
        "direction": direction
    })


def get_controller_app() -> Sanic:
    app = Sanic("ElevatorCtl")
    config_file = Path("src", "settings", "config_base.py")
    app.config.from_pyfile(config_file)
    if conf_env_var_name in os.environ:
        app.config.from_envvar(conf_env_var_name)
    app.blueprint(ev_ctl_web_bp)
    return app


app = get_controller_app()


if __name__ == "__main__":
    app.run(
        host=app.config.CONTROLLER_HOST,
        port=app.config.CONTROLLER_PORT,
        debug=app.config.DEBUG,
        protocol=WebSocketProtocol
    )

