import pymunk


class Wall:
    def __init__(self, space, p1, p2):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, p1, p2, 5)
        self.shape.elasticity = 1
        space.add(self.shape, self.body)
