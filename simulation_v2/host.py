import random

import numpy as np
import pygame
import pymunk
import sys
from abstract_infected import AbstractInfected
from constants import get_per_second, MULTIPLICATION_THRESHOLD, SIM_BOARD_SIZE_Y, SIM_BOARD_SIZE_X, random_x_in_board, \
    random_y_in_board
from ctx import ctx

thismodule = sys.modules[__name__]
thismodule.foo = 1


def update_foo():
    thismodule.foo = thismodule.foo + 10


class Host(AbstractInfected):
    def __init__(self, space, display_front, x, y, i, hosts, host_multiply, health=100):
        super().__init__(space, display_front, x, y, i, pymunk.Body(), 4, (255, 255, 255), health=health)
        self.hosts = hosts
        self.speed = 80
        self.visual_range = 50
        self.random_move()
        update_foo()
        self.a = thismodule.foo
        self.host_multiply = host_multiply

    def __eq__(self, other):
        return self.a == other.a

    def __ne__(self, other):
        return not self.__eq__(other)

    def pass_time(self) -> None:
        if self.body.position.x > SIM_BOARD_SIZE_X or self.body.position.y > SIM_BOARD_SIZE_Y:
            self.body.position.x = random_x_in_board()
            self.body.position.y = random_y_in_board()
        if self.health > 0:
            current_vector = self.body.velocity
            current_speed = np.linalg.norm(current_vector)
            if current_speed < self.speed:
                self.random_move()
            self.health -= get_per_second()
        else:
            self.shape.collision_type = ctx.die_type_collision
            self.die()
        if self.parasite:
            for parasite in self.parasite:
                pass
                self.health -= parasite.needs * get_per_second()

    def die(self) -> None:
        self.body.velocity = 0, 0
        self.visual_range = 0
        self.color = (255, 0, 0)
        self.is_alive = False

    def multiply(self, space, arbiter, data) -> bool:
        if self.health > MULTIPLICATION_THRESHOLD:
            self.health -= MULTIPLICATION_THRESHOLD / 2
            self.host_multiply.multiply_host(self)
        return False

    def eat(self, space, arbiter, data) -> bool:
        food = data['food']
        foods = data['foods']
        if food in foods:
            foods.remove(food)
            self.health += food.nutrition
            if food.parasite:
                self.catch_parasite()
        return False

    def random_move(self) -> None:
        self.body.velocity = self.random_vector()

    def random_vector(self) -> list:
        random_vector = np.array([random.uniform(-100, 100), random.uniform(-100, 100)])
        current_speed = np.linalg.norm(random_vector)
        vector_speed = self.speed * random_vector / current_speed
        return vector_speed.tolist()

    def find_nearest(self, targets) -> object:
        if self.health > 0:
            vector_to_food = self.random_vector()
            if not targets:
                return False
            min_length = 10000000
            length = None
            tmp = None
            speed_boost = 1.
            for target in targets:
                if hasattr(target, "speed"):
                    speed_boost = 1.5
                    vector = np.array(
                        [target.body.position.x - self.body.position.x, target.body.position.y - self.body.position.y])
                    if np.linalg.norm(vector) < 0.5:
                        self.multiply(None, None, None)
                else:
                    vector = np.array([target.x - self.body.position.x, target.y - self.body.position.y])
                length = np.linalg.norm(vector)
                if length < min_length and length < self.visual_range:
                    min_length = length
                    versor = self.speed * speed_boost * vector / length
                    vector_to_food = versor.tolist()
                    tmp = target
            if min_length < 10000000:
                self.body.velocity = vector_to_food
                if length is not None and length < self.visual_range:
                    return tmp
                else:
                    return None
            else:
                return None

    def draw(self) -> None:
        super().draw()
        x, y = self.body.position
        pygame.draw.circle(self.display_front, (255, 255, 255), (int(x), int(y)), self.visual_range)

    def has_parasite(self) -> bool:
        return len(self.parasite) != 0
