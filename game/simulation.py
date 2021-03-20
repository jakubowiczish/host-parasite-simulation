import random

import pygame

from game.constants import board_size_x, board_size_y, population, food_init_number, FPS
from game.food import Food
from game.host import Host
from game.wall import Wall


class Simulation:

    def __init__(self, sim_space, sim_display, sim_clock):
        self.clock = sim_clock
        self.space = sim_space
        self.display = sim_display

        self.hosts = [Host(self.space, self.display, random.randint(0, board_size_x), random.randint(0, board_size_y), i + 1)
                      for i in range(population)]

        self.foods = [Food(self.space, self.display, random.randint(0, board_size_x), random.randint(0, board_size_y), i + 1)
                      for i in range(population, population + food_init_number)]

        self.walls = [Wall(self.space, (0, 0), (0, board_size_y)),
                      Wall(self.space, (0, 0), (board_size_x, 0)),
                      Wall(self.space, (0, board_size_y), (board_size_x, board_size_y)),
                      Wall(self.space, (board_size_x, 0), (board_size_x, board_size_y))
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
