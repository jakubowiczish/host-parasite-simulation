import pygame
import pymunk


class Food:
    def __init__(self, space, display, x, y, i):
        self.display = display
        self.x = x
        self.y = y
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, 5)
        self.shape.density = 1
        self.shape.elasticity = 1
        self.shape.collision_type = i
        self.nutrition = 4
        space.add(self.body, self.shape)

    def draw(self):
        x, y = self.body.position
        pygame.draw.circle(self.display, (0, 255, 255), (int(x), int(y)), 10)
