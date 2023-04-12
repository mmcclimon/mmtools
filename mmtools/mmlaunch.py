import argparse
import os

import mmtools.util as util


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
        mongo_path = util.find_mongo_path(version)

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
            mlaunch_args.extend(["--binarypath", str(mongo_path)])
            mlaunch_args.extend(["--port", str(util.available_port_range())])
            if topology == "rs":
                mlaunch_args.append("--replicaset")
            else:
                mlaunch_args.extend(["--shards", "2", "--replicaset"])

        print("exec: " + " ".join(mlaunch_args))
        os.execvp("mlaunch", mlaunch_args)


def run():
    return MMLaunch().run()
