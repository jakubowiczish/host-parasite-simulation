import pymunk

from abstract_infected import AbstractInfected


class Food(AbstractInfected):
    def __init__(self, space, display_front, x, y, i):
        super().__init__(space, display_front, x, y, i, pymunk.Body(body_type=pymunk.Body.STATIC), 5, (0, 255, 255))
        self.nutrition = 10
