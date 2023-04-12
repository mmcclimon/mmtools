import argparse
import json
import itertools
from pathlib import Path
import re
import subprocess
import sys
from typing import NoReturn

from mmtools.environment import Environment

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


def find_mongo_path(want_version) -> str:
    if re.fullmatch(r"\d+\.\d+", want_version) is None:
        exit("error parsing version: must be X.Y")

    try:
        ret = subprocess.run(
            ["m", "installed", "--json"], check=False, capture_output=True
        )
        data = json.loads(ret.stdout)
    except BaseException as err:
        exit(f"error getting installed mongo versions from m: {err}")

    for have in data:
        if have["name"].startswith(want_version):
            return have["path"]

    have = ", ".join(map(lambda v: v["name"], data))
    exit(f"could not find matching version for {want_version}\nhave: {have}")


def exit(msg, code: int = 1) -> NoReturn:
    print(msg, file=sys.stderr)
    sys.exit(code)


# for ports: get all known environments, pick a free 15-port range
def available_port_range() -> int:
    ports_in_use = set(map(lambda e: e.starting_port(), known_environments()))
    for port in itertools.count(PORT_START, 15):
        if port not in ports_in_use:
            return port

    raise RuntimeError("could not find available port")


def known_environments() -> list[Environment]:
    return [
        Environment(d)
        for d in MMTOOLS_HOME.iterdir()
        if d.joinpath(".mlaunch_startup").is_file()
    ]
