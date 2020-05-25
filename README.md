## Elevators
An elevator simulator using Sanic and websockets

Run the ElevatorController web/websockets app with
    `python src/main.py controller start`

Run an instance of the ElevatorInstance websockets app with
    `python src/main.py elevator start`

### Settings
To override settings in `src/settings/config_base.py`, make your own config file
and use the `ELEVATOR_SETTINGS` env var to specify the path to the file.

We recommend using `config_overrides.py` in the `settings` directory
and specifying it as such (if your are on a *Nix) system

`export ELEVATOR_SETTINGS=.../src/settings/config_overrides.py` 

- `MIN_STATUS_WAIT`: minimum number of seconds each elevator instance waits
    between sending status updates to the controller