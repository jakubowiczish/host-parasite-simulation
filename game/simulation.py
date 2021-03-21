import pygame

from game.constants import SIM_BOARD_SIZE_X, SIM_BOARD_SIZE_Y, POPULATION, FOOD_INIT_NUMBER, FPS, random_x_in_board, \
    random_y_in_board, ALL_HANDLERS, increment_handlers, get_per_second
from game.food import Food
from game.food_spawn import FoodSpawn
from game.host import Host
from game.parasite import Parasite
from game.wall import Wall


class Simulation:

    def __init__(self, space, display, clock, display_front):
        self.clock = clock
        self.space = space
        self.display = display
        self.display_front = display_front
        self.hosts = [
            Host(self.space, self.display, self.display_front, random_x_in_board(), random_y_in_board(), i + 1, None)
            for i in range(POPULATION)]
        for host in self.hosts:
            host.hosts = self.hosts
        self.foods = [
            Food(self.space, self.display, self.display_front, random_x_in_board(), random_y_in_board(), i + 1)
            for i in range(POPULATION, POPULATION + FOOD_INIT_NUMBER)]
        self.spawn_food = FoodSpawn(display, display_front, space, self.foods, self.hosts)
        self.hosts[0].catch_parasite()
        self.walls = [
            Wall(self.space, (0, 0), (0, SIM_BOARD_SIZE_Y)),
            Wall(self.space, (0, 0), (SIM_BOARD_SIZE_X, 0)),
            Wall(self.space, (0, SIM_BOARD_SIZE_Y), (SIM_BOARD_SIZE_X, SIM_BOARD_SIZE_Y)),
            Wall(self.space, (SIM_BOARD_SIZE_X, 0), (SIM_BOARD_SIZE_X, SIM_BOARD_SIZE_Y))
        ]

    def pass_time(self):
        self.spawn_food.spawn_food_random()

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
            pygame.display.update()
            self.clock.tick(FPS)
            self.space.step(get_per_second())
