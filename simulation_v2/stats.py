import pygame

from constants import SIM_BOARD_SIZE_X
from ctx import ctx


class Stats:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 70)

    def print_stats(self, text, x=SIM_BOARD_SIZE_X, y=100, color=(255, 255, 255)):
        text_obj = self.font.render(text, True, color)
        text_rect = text_obj.get_rect()
        text_rect.topleft = (x, y)
        ctx.display.blit(text_obj, text_rect)
