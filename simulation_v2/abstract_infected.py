import pygame
import pymunk

from ctx import ctx
from parasite import Parasite


class AbstractInfected(object):
    def __init__(self, space, display_front, x, y, i, body, size, color, health=100):
        self.display_front = display_front
        self.x = x
        self.y = y
        self.body = body
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, size)
        self.shape.density = 1
        self.shape.elasticity = 1
        self.shape.collision_type = i
        self.health = health
        self.size = size
        self.parasite = []
        self.color = color
        self.space = space
        self.is_alive = True
        space.add(self.body, self.shape)

    def draw(self):
        x, y = self.body.position
        pygame.draw.circle(ctx.display, self.color, (int(x), int(y)), self.size)

    def catch_parasite(self):
        self.color = (self.color[0], self.color[1], 100)
        self.parasite.append(Parasite())
