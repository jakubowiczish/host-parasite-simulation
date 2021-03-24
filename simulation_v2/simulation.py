from typing import Callable

import pygame as pg

from config import config
from ctx import ctx
from food import Food
from food_spawn import FoodSpawn
from game.constants import SIM_BOARD_SIZE_X, SIM_BOARD_SIZE_Y, POPULATION, FOOD_INIT_NUMBER, FPS, random_x_in_board, \
    random_y_in_board, get_per_second
from host import Host
from host_multiplayer import HostMultiplayer
from state import State
from stats import Stats
from wall import Wall


class Simulation(State):

    def __init__(self):
        self.display = ctx.display
        pg.display.set_caption(config.window_title)
        self.clock = ctx.clock
        self.space = ctx.space
        self.display_front = ctx.surface
        self.host_multiply = HostMultiplayer(self.display, self.display_front, self.space, None, None)
        self.hosts = [
            Host(self.space, self.display, self.display_front, random_x_in_board(), random_y_in_board(), i + 1, None,
                 self.host_multiply)
            for i in range(POPULATION)]
        for host in self.hosts:
            host.hosts = self.hosts
        self.foods = [
            Food(self.space, self.display, self.display_front, random_x_in_board(), random_y_in_board(), i + 1)
            for i in range(POPULATION, POPULATION + FOOD_INIT_NUMBER)]
        self.host_multiply.hosts = self.hosts
        self.host_multiply.foods = self.foods
        self.spawn_food = FoodSpawn(self.display, self.display_front, self.space, self.foods, self.hosts)
        self.hosts[0].catch_parasite()
        self.walls = [
            Wall(self.space, (0, 0), (0, SIM_BOARD_SIZE_Y)),
            Wall(self.space, (0, 0), (SIM_BOARD_SIZE_X, 0)),
            Wall(self.space, (0, SIM_BOARD_SIZE_Y), (SIM_BOARD_SIZE_X, SIM_BOARD_SIZE_Y)),
            Wall(self.space, (SIM_BOARD_SIZE_X, 0), (SIM_BOARD_SIZE_X, SIM_BOARD_SIZE_Y))
        ]
        self.stats = Stats(self.display)

        self.finished = False
        self.pause = False

    def draw_walls(self) -> None:
        line_color = (48, 48, 48)
        border_color = (192, 192, 192)

        pg.draw.line(ctx.surface, line_color, (0, 0), (0, SIM_BOARD_SIZE_Y), 20)
        pg.draw.line(ctx.surface, line_color, (0, 0), (SIM_BOARD_SIZE_X, 0), 20)
        pg.draw.line(ctx.surface, border_color, (0, SIM_BOARD_SIZE_Y), (SIM_BOARD_SIZE_X, SIM_BOARD_SIZE_Y), 20 + 2)
        pg.draw.line(ctx.surface, border_color, (SIM_BOARD_SIZE_X, 0), (SIM_BOARD_SIZE_X, SIM_BOARD_SIZE_Y), 20 + 2)

    def initialize(self) -> None:
        for host in self.hosts:
            for food in self.foods:
                handler = self.space.add_collision_handler(host.shape.collision_type, food.shape.collision_type)
                handler.data['food'] = food
                handler.data['foods'] = self.foods
                handler.begin = host.eat

    def is_finished(self) -> bool:
        return self.finished

    def draw(self) -> None:
        self.draw_walls()

    def pass_time(self):
        self.spawn_food.spawn_food_random()

    def update(self, switch_state: Callable) -> None:
        self.display.fill((0, 0, 0))
        self.display_front.fill((0, 0, 0))
        self.display_front.set_alpha(128)

        for host in self.hosts:
            host.find_nearest_food(self.foods)
            host.draw()
            host.pass_time()
        for food in self.foods:
            food.draw()
        self.pass_time()
        self.display.blit(self.display_front, (0, 0))
        # self.stats.print_stats('Statistics')
        self.stats.print_stats(f"There is {len(self.foods)} food ")
        pg.display.update()
        self.clock.tick(FPS)
        self.space.step(get_per_second())
