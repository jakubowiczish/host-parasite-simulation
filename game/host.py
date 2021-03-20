import numpy as np
import pygame
import pymunk
import random

from game.constants import DIE_TYPE_COLLISION, FPS


class Host:
    def __init__(self, space, display, x, y, i):
        self.display = display
        self.x = x
        self.y = y
        self.body = pymunk.Body()
        self.body.position = x, y
        self.body.velocity = random.uniform(-100, 100), random.uniform(-100, 100)
        self.shape = pymunk.Circle(self.body, 10)
        self.shape.density = 1
        self.shape.elasticity = 1
        self.shape.collision_type = i
        self.infected_time = 0
        self.infected = False
        self.recovered = False
        self.health = 100
        space.add(self.body, self.shape)

    def pass_time(self):
        print(self.health)
        if self.health > 0:
            self.health -= 1 / FPS
        else:
            self.shape.collision_type = DIE_TYPE_COLLISION
            self.die()

    def die(self):
        self.body.velocity = 0, 0

    def draw(self):
        x, y = self.body.position
        if self.health == 0:
            pygame.draw.circle(self.display, (255, 0, 0), (int(x), int(y)), 10)
        else:
            pygame.draw.circle(self.display, (255, 255, 255), (int(x), int(y)), 10)

    def eat(self, space, arbiter, data):
        food = data['food']
        foods = data['foods']
        if food in foods:
            foods.remove(food)
            self.health += food.nutrition
        return False

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
