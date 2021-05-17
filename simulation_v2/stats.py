from constants import STATS_Y_POSITION, STATS_X_POSITION
from text import Text


class Stats:

    @staticmethod
    def draw(food_amount, parasites_amount, hosts_amount):
        Text.draw(f"Food: {food_amount}", centerx=STATS_X_POSITION, top=STATS_Y_POSITION, color="gold")
        Text.draw(f"Parasites in hosts: {parasites_amount}", centerx=STATS_X_POSITION, top=STATS_Y_POSITION + 100,
                  color="gold")
        Text.draw(f"Hosts: {hosts_amount}", centerx=STATS_X_POSITION, top=STATS_Y_POSITION + 200, color="gold")
