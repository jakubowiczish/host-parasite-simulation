import toml

from resources import path


class Config:
    def __init__(self) -> None:
        with open(path("simulation_config.toml"), "r") as f:
            self.toml = toml.loads(f.read())

        self.window_size = (
            self.toml["window"]["width"],
            self.toml["window"]["height"],
        )

        self.background_color = self.toml["window"]["background_color"]
        self.window_title = self.toml["window"]["window_title"]
        self.device = self.toml["input"]["controls"]


config = Config()
