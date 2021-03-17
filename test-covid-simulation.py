import pygame
import random
import pymunk
import numpy as np

pygame.init()

size_x = 800
size_y = 800

display = pygame.display.set_mode((size_x, size_y))
clock = pygame.time.Clock()
FPS = 90
space = pymunk.Space()

population = 2
food_init_number = 20

recovery_time = 300  # dependent on fps


class Host:
    def __init__(self, x, y, i):
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

    def eat(self, space, arbiter, data):
        food = data['food']
        foods = data['foods']
        if food in foods:
            foods.remove(food)
        return False

    def find_nearest_food(self, foods):
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


class Wall:
    def __init__(self, p1, p2):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, p1, p2, 5)
        self.shape.elasticity = 1
        space.add(self.shape, self.body)


class Food:
    def __init__(self, x, y, i):
        self.x = x
        self.y = y
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, 5)
        self.shape.density = 1
        self.shape.elasticity = 1
        self.shape.collision_type = i
        space.add(self.body, self.shape)

    def draw(self):
        x, y = self.body.position
        pygame.draw.circle(display, (0, 255, 255), (int(x), int(y)), 10)


def game():
    balls = [Host(random.randint(0, size_x), random.randint(0, size_y), i + 1) for i in range(population)]
    foods = [Food(random.randint(0, size_x), random.randint(0, size_y), i + 1) for i in
             range(population, population + food_init_number)]

    for ball in balls:
        for food in foods:
            handler = space.add_collision_handler(ball.shape.collision_type, food.shape.collision_type)
            handler.data['food'] = food
            handler.data['foods'] = foods
            handler.begin = ball.eat

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
            ball.find_nearest_food(foods)
            ball.draw()
            ball.pass_time()
        for food in foods:
            food.draw()

        pygame.display.update()
        clock.tick(FPS)
        space.step(1 / FPS)


if __name__ == '__main__':
    game()
    pygame.quit()
