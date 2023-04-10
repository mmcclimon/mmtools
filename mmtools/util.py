import argparse
import json
from pathlib import Path

MMTOOLS_HOME = Path.home().joinpath(".mmtools")
PORT_START = 27110


def add_common_args(parser: argparse.ArgumentParser) -> None:
    """
    Add the global args we need everywhere to the provided parser.
    """
    parser.add_argument(
        "-v", "--version", default="6.0", help="mongodb version to use (X.Y)"
    )

    kind = parser.add_mutually_exclusive_group()
    kind.add_argument("--rs", help="use a replica set", action="store_true")
    kind.add_argument("--sc", help="use a sharded cluster", action="store_true")

    target = parser.add_mutually_exclusive_group()
    target.add_argument(
        "--src", "-s", help="target a source cluster", action="store_true"
    )
    target.add_argument(
        "--dst", "-d", help="target a destination cluster", action="store_true"
    )

    return


# for ports: get all known environments, pick a free 15-port range
def available_port_range() -> int:
    # for every environment, read its port number out of the mlaunch startup
    # file
    ports_in_use = list(sorted(map(port_for_environment, known_environments())))
    print(ports_in_use)
    return 0


def port_for_environment(envdir: Path) -> int:
    with open(envdir.joinpath('.mlaunch_startup')) as f:
        data = json.load(f)
        return data['parsed_args']['port']


def known_environments() -> list[Path]:
    known = []
    for d in MMTOOLS_HOME.iterdir():
        if d.joinpath('.mlaunch_startup').is_file():
            known.append(d)

    return known
