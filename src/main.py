"""CLI tool for controlling the elevator simulator"""
from argparse import ArgumentParser
from pathlib import Path
import sys

sys.path.append(str(Path.cwd()))


def build_base_parser() -> ArgumentParser:
    arg_parser = ArgumentParser()
    subparsers = arg_parser.add_subparsers()
    ev_instance_parser = subparsers.add_parser(
        "elevator", help="Elevator instance commands"
    )
    build_elevator_instance_parser(ev_instance_parser)
    controller_parser = subparsers.add_parser("controller", help="Controller commands")
    build_controller_parser(controller_parser)
    return arg_parser


def build_elevator_instance_parser(sub_parser: ArgumentParser):
    sub_parser.add_argument(
        "ev_command", choices=["start"], help="Controller command to run"
    )


def build_controller_parser(sub_parser: ArgumentParser):
    sub_parser.add_argument(
        "ctl_command", choices=["start"], help="Elevator command to run"
    )


if __name__ == "__main__":
    from src.elevators.instance_ws import run_elevator
    from src.controller.controller_app import run_controller

    parser = build_base_parser()
    args: dict = vars(parser.parse_args())
    if args.get("ev_command") == "start":
        run_elevator()
    elif args.get("ctl_command") == "start":
        run_controller()
