from game.abstract_infected import AbstractInfected


class Food(AbstractInfected):
    def __init__(self, space, display, x, y, i):
        super().__init__(space, display, x, y, i, 5, (0, 255, 255))
        self.nutrition = 4
