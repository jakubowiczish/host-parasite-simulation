from typing import Any, Callable, List, MutableMapping, Optional

import pygame as pg
import toml

from config import config
from ctx import ctx
from device import Device
from input import Input
from resources import path
from state import State
from text import Text


class Prompter(State):
    def __init__(self, state: State) -> None:
        self.state = state
        self.controls: MutableMapping[str, Any] = dict()
        self.finished = False
        self.started = ctx.now

    def is_finished(self) -> bool:
        return self.finished

    def initialize(self) -> None:
        with open(path("controls.toml"), "r") as f:
            self.controls = toml.loads(f.read())

    def update(self, switch_state: Callable) -> None:
        device = self.get_active_device()
        if device is not None:
            switch_state(self.state)

    def draw(self) -> None:
        Text.draw(
            "Press any button",
            size=5,
            gcolor="red",
            centery=350,
            centerx=650,
        )

    def get_active_device(self) -> Optional[Device]:
        devices: List[Device] = list()
        pg.event.pump()

        device_names = [config.device]
        for device_name in device_names:
            if self.controls[device_name]["type"] == "keyboard":
                devices += [Device(device_name)]

        inputs: List[Input] = list()
        for device in devices:
            inputs += [Input(device)]

        for input in inputs:
            if input.update():
                return input.device

        return None
