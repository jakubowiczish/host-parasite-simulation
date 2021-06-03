import time

import pygame as pg
import pymunk as pm


class Context:
    def __init__(self) -> None:
        self.running = True
        self.now: float
        self.simulation_start_time: float
        self.surface: pg.surface.Surface
        self.space: pm.Space
        self.display: pg.display
        self.population: int
        self.food_amount: int
        self.speedup: int
        self.die_type_collision: int
        self.food_spawn_interval: int
        self.infected_food_chance: float
        self.all_handlers: int
        self.food_amount_per_simulation_step: int

    @staticmethod
    def re_init(population, food_amount, speedup, food_spawn_interval, infected_food_chance, food_amount_per_simultion_step) -> None:
        ctx.running = True
        ctx.simulation_start_time = time.monotonic()
        ctx.population = population
        ctx.food_amount = food_amount
        ctx.speedup = speedup
        ctx.die_type_collision = ctx.population + ctx.food_amount + 1
        ctx.food_spawn_interval = food_spawn_interval
        ctx.infected_food_chance = infected_food_chance
        ctx.all_handlers = ctx.die_type_collision + 1
        ctx.food_amount_per_simulation_step = food_amount_per_simultion_step


ctx = Context()
ctx.population = 2
ctx.food_amount = 40
ctx.speedup = 1
ctx.die_type_collision = ctx.population + ctx.food_amount + 1
ctx.food_spawn_interval = 3
ctx.infected_food_chance = 0.4
ctx.all_handlers = ctx.die_type_collision + 1
ctx.food_amount_per_simulation_step = 1
