import pygame

from game.constants import increment_handlers, random_x_in_board, random_y_in_board, FOOD_SPAWN_INTERVAL
from game.food import Food


class FoodSpawn:
    def __init__(self, display, space, foods, hosts):
        self.last = pygame.time.get_ticks()
        self.cool_down = FOOD_SPAWN_INTERVAL
        self.display = display
        self.space = space
        self.foods = foods
        self.hosts = hosts

    def spawn_food_random(self):
        if len(self.foods) < 2:
            now = pygame.time.get_ticks()
            if now - self.last >= self.cool_down:
                self.last = now
                self.spawn_food(random_x_in_board(), random_y_in_board())

    def spawn_food(self, x, y):
        handler_index = increment_handlers()
        random_food = Food(self.space, self.display, x, y, handler_index)
        self.foods.append(random_food)
        for host in self.hosts:
            handler = self.space.add_collision_handler(host.shape.collision_type, random_food.shape.collision_type)
            handler.data['food'] = random_food
            handler.data['foods'] = self.foods
            handler.begin = host.eat