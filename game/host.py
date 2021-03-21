import numpy as np
import pygame
import pymunk
import random

from game.abstract_infected import AbstractInfected
from game.constants import DIE_TYPE_COLLISION, FPS, get_per_second


class Host(AbstractInfected):
    def __init__(self, space, display, x, y, i):
        super().__init__(space, display, x, y, i, 10, (255, 255, 255))
        self.random_move()

    def pass_time(self):
        if self.health > 0:
            self.health -= get_per_second()
        else:
            self.shape.collision_type = DIE_TYPE_COLLISION
            self.die()
        if self.parasite:
            self.health -= self.parasite.needs * get_per_second()

    def die(self):
        self.body.velocity = 0, 0
        self.color = (255, 0, 0)

    def eat(self, space, arbiter, data):
        food = data['food']
        foods = data['foods']
        if food in foods:
            foods.remove(food)
            self.health += food.nutrition
        return False

    def random_move(self):
        self.body.velocity = random.uniform(-100, 100), random.uniform(-100, 100)

    def find_nearest_food(self, foods):
        if self.health > 0:
            vector_to_food = random.uniform(-100, 100), random.uniform(-100, 100)
            if not foods:
                return vector_to_food
            min_length = 10000000
            speed = 80
            for food in foods:
                vector = np.array([food.x - self.body.position.x, food.y - self.body.position.y])
                length = np.linalg.norm(vector)
                if length < min_length:
                    min_length = length
                    versor = speed * vector / length
                    vector_to_food = versor.tolist()

            self.body.velocity = vector_to_food
