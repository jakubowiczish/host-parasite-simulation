from typing import Callable, Dict, List

import pygame as pg

from device import Device
from keyboard import Keyboard


class Input:
    def __init__(self, device: Device) -> None:
        self.device = device
        self.type = device.type

        self.binds: Dict[str, Callable] = dict()

        if device.type == "keyboard":
            self.keyboard = Keyboard()

            for action, how in device.actions.items():
                if type(how) is str:
                    self.keyboard.bind(Input.str_to_key(how), action)
                elif type(how) is list and "repeat" in how:
                    self.keyboard.bind(Input.str_to_key(how[0]), action, True)
                else:
                    raise Exception("invalid binding: {}".format(how))

    def bind(self, binds: Dict[str, Callable]) -> None:
        self.binds = binds

    def update(self) -> List[str]:
        if self.type == "dummy":
            return []

        actions: List[str] = list()
        if self.type == "keyboard":
            actions = self.keyboard.update()

        for action in actions:
            if action in self.binds:
                self.binds[action]()

        return actions

    @staticmethod
    def str_to_key(key: str) -> int:
        keys = {
            "esc": pg.K_ESCAPE,
            "enter": pg.K_RETURN,
            "up": pg.K_UP,
            "down": pg.K_DOWN,
            "right": pg.K_RIGHT,
            "left": pg.K_LEFT,
            "space": pg.K_SPACE,
        }

        if key in keys:
            return keys[key]
        else:
            raise Exception("invalid key: {}".format(key))
