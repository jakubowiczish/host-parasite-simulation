import random

import pygame

WINDOW_SIZE_X = 1600
WINDOW_SIZE_Y = 900
SIM_BOARD_SIZE_X = 800
SIM_BOARD_SIZE_Y = 800

BOARD_START_X = 20
BOARD_START_Y = 20

STATS_X_POSITION = SIM_BOARD_SIZE_X + 300
STATS_Y_POSITION = WINDOW_SIZE_Y / 4

FPS = 60
SPEEDUP = 3

POPULATION = 2
FOOD_INIT_NUMBER = 40
DIE_TYPE_COLLISION = POPULATION + FOOD_INIT_NUMBER + 1
ALL_HANDLERS = DIE_TYPE_COLLISION + 1
RECOVERY_TIME = 300  # dependent on fps
FOOD_SPAWN_INTERVAL = 3

MAX_FOOD = 45
MULTIPLICATION_THRESHOLD = 120

INFECTED_FOOD_CHANCE = 0.4

def get_per_second():
    return (1 / FPS) * SPEEDUP


def get_time_in_seconds():
    return pygame.time.get_ticks() / 1000


def increment_handlers():
    global ALL_HANDLERS
    ALL_HANDLERS += 1
    return ALL_HANDLERS


def random_x_in_board():
    return random.randint(BOARD_START_X, SIM_BOARD_SIZE_X)


def random_y_in_board():
    return random.randint(BOARD_START_Y, SIM_BOARD_SIZE_Y)
