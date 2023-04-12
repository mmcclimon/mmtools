import argparse
import json
import os
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

        root = util.MMTOOLS_HOME
        path = "-".join([topology, version, target])
        mlaunch_dir = root.joinpath(path)

        is_init = "init" in argv

        mlaunch_args = [
            "mlaunch",
            *argv,
            "--dir",
            str(mlaunch_dir),
        ]

        if is_init:
            mlaunch_args.append("--replicaset" if topology == "rs" else "--sharded")
            mlaunch_args.extend(["--binarypath", str(mongo_path)])
            mlaunch_args.extend(["--port", str(util.available_port_range())])

        print("exec: " + " ".join(mlaunch_args))
        os.execvp("mlaunch", mlaunch_args)

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
