"""Utilities used by multiple apps"""
import os
from pathlib import Path
import socket
from typing import Optional, Union

from sanic.config import Config

__all__ = ["get_open_port", "get_ws_uri", "get_settings"]


def get_settings() -> Config:
    config_path = Path("src", "settings", "config_base.py")
    config = Config()
    config.from_pyfile(config_path)
    conf_env_var_name = config.CONF_ENV_VAR_NAME
    if conf_env_var_name in os.environ:
        config.from_envvar(conf_env_var_name)
    return config


def get_ws_uri(host: str, port: Union[str, int], path: Optional[str] = None) -> str:
    """Build a websocket URI from the input parameters"""
    return f"ws://{host}:{port}/{path}"


# TODO: import port selection
def get_open_port() -> int:
    """Gets a random open port ...for now"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port
