import json
from pathlib import Path


class Environment:
    def __init__(self, path: Path):
        self.path = path
        self._meta = None

    def __repr__(self) -> str:
        ppath = str(self.path).replace(str(Path.home()), "~")
        return f"<Environment dir={ppath}>"

    @property
    def meta(self):
        if self._meta is None:
            with open(self.path.joinpath(".mlaunch_startup")) as f:
                self._meta = json.load(f)

        return self._meta

    def starting_port(self) -> int:
        return self.meta["parsed_args"]["port"]
