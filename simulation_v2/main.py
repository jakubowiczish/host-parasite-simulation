import time

import pygame as pg
import pygame.freetype
import pymunk as pm
import ptext
import resources

from config import config
from ctx import ctx
from main_menu import MainMenu
from text import Text
from state import State


class Main:

    def __init__(self):
        self.display: pg.Surface
        self.state: State

    def switch_state(self, state: State) -> None:
        self.state = state
        self.state.initialize()

    def handle_events(self) -> bool:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                ctx.running = False
                return False

        return True

    def draw_fps(self, fps_clock):
        fps = "FPS: " + "{0:.1f}".format(fps_clock.get_fps())
        Text.draw(fps, (10, 10), size=2, alpha=0.5, color="gray")

    def run(self):
        pg.init()
        pg.font.init()
        pg.freetype.init()

        ctx.surface = pg.Surface(config.window_size, pg.SRCALPHA)
        ctx.space = pm.Space()

        self.display = pg.display.set_mode(config.window_size)
        pg.display.set_caption("Host Parasite Simulation")
        ctx.display = self.display

        ptext.FONT_NAME_TEMPLATE = resources.path("%s.ttf")

        self.switch_state(MainMenu())
        fps_clock = pg.time.Clock()
        while ctx.running:
            if not self.handle_events():
                return

            ctx.now = time.monotonic()
            self.state.update(self.switch_state)
            pg.display.update()

            if self.state.is_finished():
                self.switch_state(MainMenu())

            ctx.surface.fill(pg.Color(*config.background_color))
            self.state.draw()
            self.draw_fps(fps_clock)

            pg.transform.scale(ctx.surface, self.display.get_size(), self.display)
            fps_clock.tick(120)


if __name__ == '__main__':
    Main().run()
    pg.quit()
