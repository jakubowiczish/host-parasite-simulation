import toml

from resources import path


class Device:
    def __init__(self, name: str):
        self.name = name

        if name == "dummy":
            self.type = "dummy"
            return

        with open(path("controls.toml"), "r") as f:
            self.toml = toml.loads(f.read())[name]

        self.type = self.toml["type"]
        self.actions = self.toml
        del self.actions["type"]
