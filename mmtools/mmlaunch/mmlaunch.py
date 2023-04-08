import argparse
import json
import pathlib
import re
import sys
import subprocess

import mmtools.util as util


def exit_with_msg(msg):
    print(msg)
    sys.exit(1)


class MMLaunch:
    def __init__(self):
        self.progname = "mmlaunch"
        self.description = "mlaunch, but with more smarts"
        self.parser = argparse.ArgumentParser(
            prog=self.progname, description=self.description
        )

        util.add_common_args(self.parser)

    def run(self):
        opts, argv = self.parser.parse_known_args()
        version = opts.version
        mongo_path = self.find_mongo_path(version)

        topology = "sc" if opts.sc else "rs"
        target = "dst" if opts.dst else "src"

        root = pathlib.Path.home().joinpath(".mlaunch")

        path = "-".join([topology, version, target])
        print(root.joinpath(path), mongo_path)

    def find_mongo_path(self, want_version):
        if re.fullmatch(r"\d+\.\d+", want_version) is None:
            exit_with_msg("error parsing version: must be X.Y")

        # this will maybe throw; that's fine, if ugly.
        ret = subprocess.run(
            ["m", "installed", "--json"], check=False, capture_output=True
        )
        data = json.loads(ret.stdout)

        for have in data:
            if have["name"].startswith(want_version):
                return have["path"]

        have = ", ".join(map(lambda v: v["name"], data))
        exit_with_msg(
            f"could not find matching version for {want_version}\nhave: {have}"
        )


if __name__ == "__main__":
    MMLaunch().run()
