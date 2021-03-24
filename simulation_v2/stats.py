import pygame

from game.constants import SIM_BOARD_SIZE_X


class Stats:
    def __init__(self, surface):
        self.font = pygame.font.SysFont(None, 70)
        self.surface = surface

    def print_stats(self, text, x=SIM_BOARD_SIZE_X, y=100, color=(255, 255, 255)):
        text_obj = self.font.render(text, True, color)
        text_rect = text_obj.get_rect()
        text_rect.topleft = (x, y)
        self.surface.blit(text_obj, text_rect)
