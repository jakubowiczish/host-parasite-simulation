import pygame
import pymunk

from game.constants import size_x, size_y
from game.simulation import Simulation

if __name__ == '__main__':
    pygame.init()

    _display = pygame.display.set_mode((size_x, size_y))
    _clock = pygame.time.Clock()
    _space = pymunk.Space()

    Simulation(_space, _display, _clock).run_simulation()
    pygame.quit()
