import random

import pygame

from game.constants import SIM_BOARD_SIZE_X, SIM_BOARD_SIZE_Y, POPULATION, FOOD_INIT_NUMBER, FPS
from game.food import Food
from game.host import Host
from game.wall import Wall


class Simulation:

    def __init__(self, space, display, clock):
        self.clock = clock
        self.space = space
        self.display = display

        self.hosts = [Host(self.space, self.display, random.randint(0, SIM_BOARD_SIZE_X), random.randint(0, SIM_BOARD_SIZE_Y), i + 1)
                      for i in range(POPULATION)]

        self.foods = [Food(self.space, self.display, random.randint(0, SIM_BOARD_SIZE_X), random.randint(0, SIM_BOARD_SIZE_Y), i + 1)
                      for i in range(POPULATION, POPULATION + FOOD_INIT_NUMBER)]

        self.walls = [
            Wall(self.space, (0, 0), (0, SIM_BOARD_SIZE_Y)),
            Wall(self.space, (0, 0), (SIM_BOARD_SIZE_X, 0)),
            Wall(self.space, (0, SIM_BOARD_SIZE_Y), (SIM_BOARD_SIZE_X, SIM_BOARD_SIZE_Y)),
            Wall(self.space, (SIM_BOARD_SIZE_X, 0), (SIM_BOARD_SIZE_X, SIM_BOARD_SIZE_Y))
        ]

    def run_simulation(self):
        for host in self.hosts:
            for food in self.foods:
                handler = self.space.add_collision_handler(host.shape.collision_type, food.shape.collision_type)
                handler.data['food'] = food
                handler.data['foods'] = self.foods
                handler.begin = host.eat

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            self.display.fill((0, 0, 0))
            for host in self.hosts:
                host.find_nearest_food(self.foods)
                host.draw()
                host.pass_time()
            for food in self.foods:
                food.draw()

            pygame.display.update()
            self.clock.tick(FPS)
            self.space.step(1 / FPS)
