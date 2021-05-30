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


ctx = Context()
ctx.population = 2
ctx.food_amount = 40
ctx.speedup = 3
