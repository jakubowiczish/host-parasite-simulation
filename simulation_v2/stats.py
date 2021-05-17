from constants import STATS_Y_POSITION, STATS_X_POSITION
from sim_data_chunk import SimDataChunk
from text import Text


class Stats:

    @staticmethod
    def draw(chunk: SimDataChunk):
        Text.draw(f"Food: {chunk.food}", centerx=STATS_X_POSITION, top=STATS_Y_POSITION, color="gold")
        Text.draw(f"Carriers: {chunk.carriers}", centerx=STATS_X_POSITION, top=STATS_Y_POSITION + 100,
                  color="gold")
        Text.draw(f"Hosts alive: {chunk.hosts_alive}", centerx=STATS_X_POSITION, top=STATS_Y_POSITION + 200,
                  color="gold")
        Text.draw(f"Hosts dead: {chunk.hosts_dead}", centerx=STATS_X_POSITION, top=STATS_Y_POSITION + 300,
                  color="gold")
