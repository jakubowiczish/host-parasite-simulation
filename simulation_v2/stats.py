from constants import STATS_Y_POSITION, STATS_X_POSITION
from text import Text


class Stats:

    @staticmethod
    def draw(food_amount, carriers_amount, hosts_alive_amount, hosts_dead_amount):
        Text.draw(f"Food: {food_amount}", centerx=STATS_X_POSITION, top=STATS_Y_POSITION, color="gold")
        Text.draw(f"Carriers: {carriers_amount}", centerx=STATS_X_POSITION, top=STATS_Y_POSITION + 100,
                  color="gold")
        Text.draw(f"Hosts alive: {hosts_alive_amount}", centerx=STATS_X_POSITION, top=STATS_Y_POSITION + 200,
                  color="gold")
        Text.draw(f"Hosts dead: {hosts_dead_amount}", centerx=STATS_X_POSITION, top=STATS_Y_POSITION + 300,
                  color="gold")
