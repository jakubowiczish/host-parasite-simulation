import pygame as pg


class Context:
    def __init__(self) -> None:
        self.running = True
        self.now: float
        self.surface: pg.surface.Surface


ctx = Context()
