import pygame
import pymunk

from game.constants import WINDOW_SIZE_X, WINDOW_SIZE_Y
from game.simulation import Simulation

if __name__ == '__main__':
    pygame.init()

    _display = pygame.display.set_mode((WINDOW_SIZE_X, WINDOW_SIZE_Y))
    _clock = pygame.time.Clock()
    _space = pymunk.Space()

    Simulation(_space, _display, _clock).run_simulation()
    pygame.quit()
