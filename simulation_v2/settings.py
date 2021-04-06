from collections import Callable

from config import config
from ctx import ctx
from device import Device
from input import Input
from prompter import Prompter
from simulation import Simulation
from state import State
from text import Text


class Settings(State):
    def __init__(self) -> None:
        self.input = Input(Device(config.device))
        self.position = 0
        self.min_position = 0
        self.max_position = 2
        self.entered = False
        self.population = 2
        self.food_amount = 40

    def is_finished(self) -> bool:
        return False

    def initialize(self) -> None:
        binds = {
            "down": self.position_down,
            "up": self.position_up,
            "select": self.position_enter,
            "esc": self.position_leave,
            "left": self.decrease,
            "right": self.increase
        }
        self.input.bind(binds)

    def position_down(self) -> None:
        self.position += 1
        if self.position > self.max_position:
            self.position = self.max_position

    def position_up(self) -> None:
        self.position -= 1
        if self.position < self.min_position:
            self.position = self.min_position
        # else:
        #     ctx.mixer.play("change")

    def position_enter(self) -> None:
        self.entered = True

    def position_leave(self) -> None:
        self.entered = False

    def increase(self) -> None:
        if self.position == 0:
            self.population += 1
            if self.population < 0:
                self.population = 0
        if self.position == 1:
            self.food_amount += 1
            if self.food_amount < 0:
                self.food_amount = 0

    def decrease(self) -> None:
        if self.position == 0:
            self.population -= 1
            if self.population < 0:
                self.population = 0
        if self.position == 1:
            self.food_amount -= 1
            if self.food_amount < 0:
                self.food_amount = 0

    def update(self, switch_state: Callable) -> None:
        self.input.update()

        if self.entered:
            # if self.position == 0:

            if self.position == 2:
                ctx.population = self.population
                ctx.food_amount = self.food_amount
                switch_state(Prompter(Simulation(ctx.population, ctx.food_amount)))

    def draw(self) -> None:
        Text.draw("Settings", centerx=640, top=30, size=3)

        colors = ["white" for _ in range(self.max_position + 1)]
        colors[self.position] = "gold"

        Text.draw("Number of hosts {}".format(self.population), centerx=650, top=300, color=colors[0])
        Text.draw("Number of food {}".format(self.food_amount), centerx=650, top=350, color=colors[0])
        Text.draw("Start simulation", centerx=650, top=400, color=colors[0])

        x = 350
        y = 305 + self.position * 50
        Text.draw("\u2192", (x, y), color="gold", size=2)
