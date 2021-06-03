from typing import Callable

import pygame as pg

from config import config
from constants import SIM_BOARD_SIZE_X, SIM_BOARD_SIZE_Y, random_x_in_board, \
    random_y_in_board, get_per_second, MULTIPLICATION_THRESHOLD
from ctx import ctx
from food import Food
from food_spawn import FoodSpawn
from host import Host
from host_multiplayer import HostMultiplier
from sim_data import sim_data
from sim_data_chunk import SimDataChunk
from simulation_v2.sim_plot import SimPlot
from state import State
from stats import Stats
from wall import Wall
import math

class Simulation(State):

    def __init__(self):
        pg.display.set_caption(config.window_title)
        self.space = ctx.space
        self.prev_chunk = None
        self.display_front = ctx.surface
        self.host_multiply = HostMultiplier(self.display_front, self.space, None, None)
        self.hosts = [
            Host(self.space, self.display_front, random_x_in_board(), random_y_in_board(), i + 1, None,
                 self.host_multiply)
            for i in range(ctx.population)
        ]
        for host in self.hosts:
            host.hosts = self.hosts
        self.foods = [
            Food(self.space, self.display_front, random_x_in_board(), random_y_in_board(), i + 1)
            for i in range(ctx.population, ctx.population + ctx.food_amount)
        ]

        self.host_multiply.hosts = self.hosts
        self.host_multiply.foods = self.foods
        self.spawn_food = FoodSpawn(self.display_front, self.space, self.foods, self.hosts)
        self.walls = [
            Wall(self.space, (20, 20), (20, SIM_BOARD_SIZE_Y)),
            Wall(self.space, (20, 20), (SIM_BOARD_SIZE_X, 20)),
            Wall(self.space, (20, SIM_BOARD_SIZE_Y), (SIM_BOARD_SIZE_X, SIM_BOARD_SIZE_Y)),
            Wall(self.space, (SIM_BOARD_SIZE_X, 20), (SIM_BOARD_SIZE_X, SIM_BOARD_SIZE_Y))
        ]
        self.finished = False
        self.pause = False

    def draw_walls(self) -> None:
        border_color = (192, 192, 192)
        for wall in self.walls:
            pg.draw.line(ctx.surface, border_color, wall.p1, wall.p2, 20)

    def initialize(self) -> None:
        for host in self.hosts:
            other_hosts = filter(lambda x: x != host, self.hosts)
            for other_host in other_hosts:
                handler_host = self.space.add_collision_handler(host.shape.collision_type, other_host.shape.collision_type)
                handler_host.begin = host.multiply
                other_handler = self.space.add_collision_handler(other_host.shape.collision_type,
                                                                 host.shape.collision_type)
                other_handler.begin = other_host.multiply
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

    def get_total_number_of_carriers(self) -> int:
        counter = 0
        for host in self.hosts:
            if host.has_parasite() and host.is_alive:
                counter += 1
        return counter

    def get_total_number_of_parasites(self) -> int:
        counter = 0
        for host in self.hosts:
            if host.is_alive:
                for parasite in host.parasite:
                    counter += 1
        return counter

    def get_total_number_of_hosts_alive(self) -> int:
        counter = 0
        for host in self.hosts:
            if host.is_alive:
                counter += 1
        return counter

    def get_total_number_of_hosts_dead(self) -> int:
        counter = 0
        for host in self.hosts:
            if not host.is_alive:
                counter += 1
        return counter

    def update(self, switch_state: Callable) -> None:
        ctx.surface.fill((0, 0, 0))
        self.display_front.fill((0, 0, 0))
        self.display_front.set_alpha(128)
        keys = pg.key.get_pressed()
        if keys[pg.K_k]:
            for host in self.hosts:
                host.die()

        for host in self.hosts:
            other_hosts = filter(lambda x: x != host and x.is_alive and host.is_alive, self.hosts)
            if host.health > MULTIPLICATION_THRESHOLD:
                target = host.find_nearest(list(other_hosts))
                if target is None:
                    host.find_nearest(self.foods)
            else:
                host.find_nearest(self.foods)
            host.draw()
            host.pass_time()
        for food in self.foods:
            food.draw()
        self.pass_time()
        current_time = ctx.now - ctx.simulation_start_time
        sim_data_chunk = SimDataChunk(
            food=len(self.foods),
            hosts_alive=self.get_total_number_of_hosts_alive(),
            hosts_dead=self.get_total_number_of_hosts_dead(),
            carriers=self.get_total_number_of_carriers(),
            parasites=self.get_total_number_of_parasites(),
            timestamp=current_time
        )
        if sim_data_chunk != self.prev_chunk:
            sim_data.update(sim_data_chunk)
            self.prev_chunk = sim_data_chunk

        if sim_data_chunk.hosts_alive == 0:
            SimPlot().plot_all()
            self.finished = True

        Stats.draw(sim_data_chunk)

        ctx.display.blit(self.display_front, (0, 0))
        # pg.display.update()
        # ctx.surface.update()
        # self.clock.tick(FPS)
        self.space.step(get_per_second())
