import random

import numpy as np
import pygame
import pymunk

from abstract_infected import AbstractInfected
from constants import DIE_TYPE_COLLISION, get_per_second, MULTIPLICATION_THRESHOLD


class Host(AbstractInfected):
    def __init__(self, space, display_front, x, y, i, hosts, host_multiply):
        super().__init__(space, display_front, x, y, i, pymunk.Body(), 10, (255, 255, 255))
        self.hosts = hosts
        self.speed = 80
        self.visual_range = 50
        self.random_move()
        self.host_multiply = host_multiply

    def pass_time(self) -> None:
        if self.health > 0:
            self.health -= get_per_second()
            if self.health > MULTIPLICATION_THRESHOLD:
                self.health -= MULTIPLICATION_THRESHOLD / 2
                self.multiply()
        else:
            self.shape.collision_type = DIE_TYPE_COLLISION
            self.die()
        if self.parasite:
            self.health -= self.parasite.needs * get_per_second()

    def die(self) -> None:
        self.body.velocity = 0, 0
        self.visual_range = 0
        self.color = (255, 0, 0)
        self.is_alive = False

    def multiply(self) -> None:
        self.host_multiply.multiply_host(self)

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
        self.body.velocity = random.uniform(-100, 100), random.uniform(-100, 100)

    def find_nearest_food(self, foods) -> None:
        if self.health > 0:
            vector_to_food = random.uniform(-100, 100), random.uniform(-100, 100)
            if not foods:
                return
            min_length = 10000000
            for food in foods:
                vector = np.array([food.x - self.body.position.x, food.y - self.body.position.y])
                length = np.linalg.norm(vector)
                if length < min_length and length < self.visual_range:
                    min_length = length
                    versor = self.speed * vector / length
                    vector_to_food = versor.tolist()
            if min_length < 10000000:
                self.body.velocity = vector_to_food

    def draw(self) -> None:
        super().draw()
        x, y = self.body.position
        pygame.draw.circle(self.display_front, (255, 255, 255), (int(x), int(y)), self.visual_range)

    def has_parasite(self) -> bool:
        return self.parasite is not None
