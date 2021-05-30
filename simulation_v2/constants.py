import random

import pygame

from ctx import ctx

WINDOW_SIZE_X = 1600
WINDOW_SIZE_Y = 900
SIM_BOARD_SIZE_X = 800
SIM_BOARD_SIZE_Y = 800

BOARD_START_X = 20
BOARD_START_Y = 20

STATS_X_POSITION = SIM_BOARD_SIZE_X + 300
STATS_Y_POSITION = WINDOW_SIZE_Y / 4

FPS = 60

MAX_FOOD = 45
MULTIPLICATION_THRESHOLD = 120


def get_per_second():
    return (1 / FPS) * ctx.speedup


def get_time_in_seconds():
    return pygame.time.get_ticks() / 1000


def increment_handlers():
    ctx.all_handlers += 1
    return ctx.all_handlers


def random_x_in_board():
    return random.randint(BOARD_START_X, SIM_BOARD_SIZE_X)


def random_y_in_board():
    return random.randint(BOARD_START_Y, SIM_BOARD_SIZE_Y)
