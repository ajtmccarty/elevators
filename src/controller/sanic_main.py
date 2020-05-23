import asyncio
import datetime
import os
from pathlib import Path
import random

from sanic import Sanic, Blueprint
from sanic.response import json
from sanic.websocket import WebSocketProtocol

conf_env_var_name = "ELEVATOR_SETTINGS"
elevator_web_bp = Blueprint("ElevatorWebController")


@elevator_web_bp.route("/button/<floor>/<direction>")
async def button(request, floor, direction):
    print(f"Received: floor: {floor}, direction: {direction}")
    return json({
        "floor": floor,
        "direction": direction
    })


if __name__ == "__main__":
    app = Sanic("Elevators")
    config_file = Path("src", "controller", "config_base.py")
    app.config.from_pyfile(config_file)
    if conf_env_var_name in os.environ:
        app.config.from_envvar(conf_env_var_name)
    app.blueprint(elevator_web_bp)
    app.run(
        host=app.config.HOST,
        port=app.config.PORT,
        debug=app.config.DEBUG,
        protocol=WebSocketProtocol
    )
