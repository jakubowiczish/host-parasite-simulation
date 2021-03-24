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
    def __init__(self, state: State, players: int) -> None:
        self.state = state

        self.controls: MutableMapping[str, Any] = dict()
        self.finished = False

        self.started = ctx.now
        self.last_joystick_refresh = 0.0

    def is_finished(self) -> bool:
        return self.finished

    def initialize(self) -> None:
        with open(path("controls.toml"), "r") as f:
            self.controls = toml.loads(f.read())

    def update(self, switch_state: Callable) -> None:
        pass

    def draw(self) -> None:
        Text.draw(
            "Press any button",
            size=5,
            gcolor="red",
            centery=350,
            centerx=650,
        )

    def get_active_device(self) -> Optional[Device]:
        if ctx.now - self.last_joystick_refresh > 1.0:
            pg.joystick.quit()
            self.last_joystick_refresh = ctx.now

        pg.joystick.init()
        devices: List[Device] = list()

        pg.event.pump()

        device_names: List[str] = list()
        if self.done_players == 0:
            device_names = [config.device1, config.device2]
        elif self.done_players == 1:
            device_names = [config.device2, config.device1]

        for device_name in device_names:
            if self.controls[device_name]["type"] == "keyboard":
                devices += [Device(device_name)]
            elif self.controls[device_name]["type"] == "joystick":
                for j in range(pg.joystick.get_count()):
                    devices += [Device(device_name, j)]

        inputs: List[Input] = list()
        for device in devices:
            inputs += [Input(device)]

        for input in inputs:
            if input.update():
                return input.device

        return None
