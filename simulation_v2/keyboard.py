from typing import Dict, List, Tuple

import pygame as pg

from config import config
from ctx import ctx

Key = int


class Keyboard:
    def __init__(self) -> None:
        self.pressed_keys: List[bool] = list()
        self.last_press: Dict[Key, float] = dict()
        self.last_repeat: Dict[Key, float] = dict()

        self.binds: Dict[Key, Tuple[str, bool]] = dict()

    def bind(self, key: Key, action: str, repeat=False) -> None:
        self.binds[key] = (action, repeat)

    def update(self) -> List[str]:
        actions: List[str] = list()

        self.pressed_keys = pg.key.get_pressed()

        for key, (action, repeat) in self.binds.items():
            if self.key_pressed(key, repeat):
                actions += [action]

        return actions

    def key_pressed(self, key: Key, repeat: bool) -> bool:
        if not self.pressed_keys[key]:
            if key in self.last_press:
                del self.last_press[key]
            if key in self.last_repeat:
                del self.last_repeat[key]
            return False

        if key not in self.last_press:
            self.last_press[key] = ctx.now
            return True

        if not repeat:
            return False

        if ctx.now - self.last_press[key] < config.key_repeat_delay:
            return False

        if key not in self.last_repeat:
            self.last_repeat[key] = ctx.now
            return True

        if ctx.now - self.last_repeat[key] < config.key_repeat_interval:
            return False

        self.last_repeat[key] = ctx.now
        return True
