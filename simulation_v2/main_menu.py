from typing import Callable

from config import config
from device import Device
from input import Input
from prompter import Prompter
from simulation import Simulation
from state import State
from text import Text


class MainMenu(State):
    def __init__(self) -> None:
        self.input = Input(Device(config.device))
        self.position = 0
        self.min_position = 0
        self.max_position = 1
        self.entered = False

    def is_finished(self) -> bool:
        return False

    def initialize(self) -> None:
        # ctx.mixer.play_music("menu_theme")
        binds = {
            "down": self.position_down,
            "up": self.position_up,
            "select": self.position_enter,
        }
        self.input.bind(binds)

    def position_down(self) -> None:
        self.position += 1
        if self.position > self.max_position:
            self.position = self.max_position
        # else:
            # ctx.mixer.play("change")

    def position_up(self) -> None:
        self.position -= 1
        if self.position < self.min_position:
            self.position = self.min_position
        # else:
        #     ctx.mixer.play("change")

    def position_enter(self) -> None:
        # ctx.mixer.play("choose")
        self.entered = True

    def update(self, switch_state: Callable) -> None:
        self.input.update()

        if self.entered:
            if self.position == 0:
                switch_state(Prompter(Simulation()))

    def draw(self) -> None:
        Text.draw("Host Parasite Simulation", centerx=640, top=30, size=3)

        colors = ["white" for _ in range(self.max_position + 1)]
        colors[self.position] = "gold"

        Text.draw("Simulation", centerx=650, top=300, color=colors[0])

        x = 460
        y = 305 + self.position * 50
        Text.draw("\u2192", (x, y), color="gold", size=2)
