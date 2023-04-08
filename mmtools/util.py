import argparse


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
