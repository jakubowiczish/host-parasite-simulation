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
        self.entered = False
        self.min_position = 0
        self.position = 0
        self.max_position = 6

        self.population = 2
        self.food_amount = 40

        self.min_speedup = 1
        self.speedup = 1
        self.max_speedup = 5

        self.min_food_spawn_interval = 0.1
        self.food_spawn_interval = 3
        self.max_food_spawn_interval = 5

        self.min_infected_food_chance = 0.1
        self.infected_food_chance = 0.4
        self.max_infected_food_chance = 0.9

        self.min_food_amount_per_simulation_step = 0
        self.food_amount_per_simulation_step = 1
        self.max_food_amount_per_simulation_step = 20

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
        if self.position == 2:
            self.speedup += 1
            if self.speedup > self.max_speedup:
                self.speedup = self.max_speedup
        if self.position == 3:
            self.food_spawn_interval += 0.1
            if self.food_spawn_interval > self.max_food_spawn_interval:
                self.food_spawn_interval = self.max_food_spawn_interval
        if self.position == 4:
            self.infected_food_chance += 0.1
            if self.infected_food_chance > self.max_infected_food_chance:
                self.infected_food_chance = self.max_infected_food_chance
        if self.position == 5:
            self.food_amount_per_simulation_step += 1
            if self.food_amount_per_simulation_step > self.max_food_amount_per_simulation_step:
                self.food_amount_per_simulation_step = self.max_food_amount_per_simulation_step

    def decrease(self) -> None:
        if self.position == 0:
            self.population -= 1
            if self.population < 0:
                self.population = 0
        if self.position == 1:
            self.food_amount -= 1
            if self.food_amount < 0:
                self.food_amount = 0
        if self.position == 2:
            self.speedup -= 1
            if self.speedup < self.min_speedup:
                self.speedup = self.min_speedup
        if self.position == 3:
            self.food_spawn_interval -= 0.1
            if self.food_spawn_interval < self.min_food_spawn_interval:
                self.food_spawn_interval = self.min_food_spawn_interval
        if self.position == 4:
            self.infected_food_chance -= 0.1
            if self.infected_food_chance < self.min_infected_food_chance:
                self.infected_food_chance = self.min_infected_food_chance
        if self.position == 5:
            self.food_amount_per_simulation_step -= 1
            if self.food_amount_per_simulation_step < self.min_food_amount_per_simulation_step:
                self.food_amount_per_simulation_step = self.min_food_amount_per_simulation_step

    def update(self, switch_state: Callable) -> None:
        self.input.update()

        if self.entered:
            if self.position == self.max_position:
                ctx.re_init(
                    population=self.population,
                    food_amount=self.food_amount,
                    speedup=self.speedup,
                    food_spawn_interval=self.food_spawn_interval,
                    infected_food_chance=self.infected_food_chance,
                    food_amount_per_simultion_step=self.food_amount_per_simulation_step
                )
                switch_state(Prompter(Simulation()))

    def draw(self) -> None:
        Text.draw("Settings", centerx=640, top=30, size=3)

        colors = ["gold" for _ in range(self.max_position + 1)]
        colors[self.position] = "gold"

        text_x = 650
        Text.draw("Number of hosts: {}".format(self.population), centerx=text_x, top=300, color=colors[0])
        Text.draw("Number of food: {}".format(self.food_amount), centerx=text_x, top=350, color=colors[0])
        Text.draw("Simulation speedup: {}".format(self.speedup), centerx=text_x, top=400, color=colors[0])
        Text.draw("Food spawn interval: {:.1f}".format(self.food_spawn_interval), centerx=text_x, top=450,
                  color=colors[0])
        Text.draw("Infected food chance: {:.1f}".format(self.infected_food_chance), centerx=text_x, top=500,
                  color=colors[0])
        Text.draw("Food amount per simulation step: {}".format(self.food_amount_per_simulation_step), centerx=text_x,
                  top=550, color=colors[0])
        Text.draw("Start simulation", centerx=text_x, top=600, color=colors[0])

        arrow_x = 150
        arrow_y = 305 + self.position * 50
        Text.draw("\u2192", (arrow_x, arrow_y), color="gold", size=2)
