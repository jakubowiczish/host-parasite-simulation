import pygame
import random
import pymunk

pygame.init()

size_x = 800
size_y = 800

display = pygame.display.set_mode((size_x, size_y))
clock = pygame.time.Clock()
FPS = 90
space = pymunk.Space()

population = 300

recovery_time = 300  # dependent on fps


class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.body = pymunk.Body()
        self.body.position = x, y
        self.body.velocity = random.uniform(-100, 100), random.uniform(-100, 100)
        self.shape = pymunk.Circle(self.body, 10)
        self.shape.density = 1
        self.shape.elasticity = 1
        self.infected_time = 0
        self.infected = False
        self.recovered = False
        space.add(self.body, self.shape)

    def pass_time(self):
        if self.infected:
            self.infected_time += 1
        if self.infected_time >= recovery_time:
            self.infected = False
            self.recovered = True
            self.shape.collision_type = population + 2

    def draw(self):
        x, y = self.body.position
        if self.infected:
            pygame.draw.circle(display, (255, 0, 0), (int(x), int(y)), 10)
        elif self.recovered:
            pygame.draw.circle(display, (0, 0, 255), (int(x), int(y)), 10)
        else:
            pygame.draw.circle(display, (255, 255, 255), (int(x), int(y)), 10)

    def infect(self, space=0, arbiter=0, data=0):
        self.infected = True
        self.shape.collision_type = population + 1


class Wall:
    def __init__(self, p1, p2):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, p1, p2, 5)
        self.shape.elasticity = 1
        space.add(self.shape, self.body)


def game():
    balls = [Ball(random.randint(0, size_x), random.randint(0, size_y)) for _ in range(population)]
    for i in range(1, population + 1):
        balls[i - 1].shape.collision_type = i
        handler = space.add_collision_handler(i, population + 1)
        handler.separate = balls[i - 1].infect

    random.choice(balls).infect()
    walls = [Wall((0, 0), (0, size_y)),
             Wall((0, 0), (size_x, 0)),
             Wall((0, size_y), (size_x, size_y)),
             Wall((size_x, 0), (size_x, size_y))
             ]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        display.fill((0, 0, 0))
        for ball in balls:
            ball.draw()
            ball.pass_time()

        pygame.display.update()
        clock.tick(FPS)
        space.step(1 / FPS)


game()
pygame.quit()
