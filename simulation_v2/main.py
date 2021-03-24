import pygame as pg
import pygame.freetype
import pymunk as pm

from config import config
from game.simulation import Simulation

if __name__ == '__main__':
    pg.init()
    pg.font.init()
    pg.freetype.init()

    display = pg.display.set_mode(config.window_size)
    pg.display.set_caption(config.window_title)
    surface = pg.Surface(config.window_size, pg.SRCALPHA)
    clock = pg.time.Clock()
    space = pm.Space()
    Simulation(space, display, clock, surface).run_simulation()
    pg.quit()
