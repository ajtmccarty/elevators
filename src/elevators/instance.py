import os
from pathlib import Path

from sanic import Sanic, Blueprint
from sanic.websocket import WebSocketProtocol

conf_env_var_name = "ELEVATOR_SETTINGS"
ev_instance_bp = Blueprint("ElevatorInstance")


@ev_instance_bp.websocket("/instruction/")
async def button(request, ws):
    instruction = await ws.recv()
    print(f"Received instruction: {instruction}")
    await ws.send("ACK")


if __name__ == "__main__":
    app = Sanic("ElevatorInstance")
    config_file = Path("src", "settings", "config_base.py")
    app.config.from_pyfile(config_file)
    if conf_env_var_name in os.environ:
        app.config.from_envvar(conf_env_var_name)
    app.blueprint(ev_instance_bp)
    app.run(
        host=app.config.ELEVATOR_HOST,
        port=app.config.ELEVATOR_PORT,
        debug=app.config.DEBUG,
        protocol=WebSocketProtocol
    )
