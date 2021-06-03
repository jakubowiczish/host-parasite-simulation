import random

from constants import increment_handlers, random_x_in_board, random_y_in_board, get_time_in_seconds, MAX_FOOD
from ctx import ctx
from food import Food


class FoodSpawn:
    def __init__(self, display_front, space, foods, hosts):
        self.last = get_time_in_seconds()
        self.cool_down = ctx.food_spawn_interval
        self.display_front = display_front
        self.space = space
        self.foods = foods
        self.hosts = hosts

    def spawn_food_random(self):
        if len(self.foods) < MAX_FOOD:
            now = get_time_in_seconds()
            if now - self.last >= self.cool_down / ctx.speedup:
                self.last = now
                for _ in range(ctx.food_amount_per_simulation_step):
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
        if random.random() < ctx.infected_food_chance:
            random_food.catch_parasite()
