import random

import pygame
import pymunk

from game.constants import size_x, size_y, board_size_x, board_size_y, population, food_init_number, FPS
from game.food import Food
from game.host import Host
from game.wall import Wall

pygame.init()

display = pygame.display.set_mode((size_x, size_y))
clock = pygame.time.Clock()
space = pymunk.Space()


def game():
    hosts = [Host(space, display, random.randint(0, board_size_x), random.randint(0, board_size_y), i + 1) for i in
             range(population)]

    foods = [Food(space, display, random.randint(0, board_size_x), random.randint(0, board_size_y), i + 1) for i in
             range(population, population + food_init_number)]
    for host in hosts:
        for food in foods:
            handler = space.add_collision_handler(host.shape.collision_type, food.shape.collision_type)
            handler.data['food'] = food
            handler.data['foods'] = foods
            handler.begin = host.eat

    walls = [Wall(space, (0, 0), (0, board_size_y)),
             Wall(space, (0, 0), (board_size_x, 0)),
             Wall(space, (0, board_size_y), (board_size_x, board_size_y)),
             Wall(space, (board_size_x, 0), (board_size_x, board_size_y))
             ]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        display.fill((0, 0, 0))
        for host in hosts:
            host.find_nearest_food(foods)
            host.draw()
            host.pass_time()
        for food in foods:
            food.draw()

        pygame.display.update()
        clock.tick(FPS)
        space.step(1 / FPS)


if __name__ == '__main__':
    game()
    pygame.quit()
