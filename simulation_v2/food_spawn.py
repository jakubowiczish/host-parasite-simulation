import random

from constants import increment_handlers, random_x_in_board, random_y_in_board, FOOD_SPAWN_INTERVAL, \
    get_time_in_seconds, MAX_FOOD, INFECTED_FOOD_CHANCE
from food import Food


class FoodSpawn:
    def __init__(self, display_front, space, foods, hosts):
        self.last = get_time_in_seconds()
        self.cool_down = FOOD_SPAWN_INTERVAL
        self.display_front = display_front
        self.space = space
        self.foods = foods
        self.hosts = hosts

    def spawn_food_random(self):
        if len(self.foods) < MAX_FOOD:
            now = get_time_in_seconds()
            if now - self.last >= self.cool_down:
                self.last = now
                self.spawn_food(random_x_in_board(), random_y_in_board())

    def spawn_food(self, x, y):
        handler_index = increment_handlers()
        random_food = Food(self.space, self.display_front, x, y, handler_index)
        self.foods.append(random_food)
        for host in self.hosts:
            handler = self.space.add_collision_handler(host.shape.collision_type, random_food.shape.collision_type)
            handler.data['food'] = random_food
            handler.data['foods'] = self.foods
            handler.begin = host.eat
        if random.random() < INFECTED_FOOD_CHANCE:
            random_food.catch_parasite()
