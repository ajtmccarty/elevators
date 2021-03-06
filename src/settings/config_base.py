DEBUG: bool = False
CONF_ENV_VAR_NAME: str = "ELEVATOR_SETTINGS"

# Controller
CONTROLLER_HOST: str = "127.0.0.1"
CONTROLLER_PORT: int = 8000

# Elevator Instances
ELEVATOR_HOST: str = CONTROLLER_HOST
# TODO: implement ELEVATOR_PORT_RANGE
MIN_STATUS_WAIT: float = 3.0

# Redis
REDIS: dict = dict(
    USERNAME="", PASSWORD="", HOST="127.0.0.1", PORT=6379,
)
