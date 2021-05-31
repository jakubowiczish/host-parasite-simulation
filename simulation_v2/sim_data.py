from sim_data_chunk import SimDataChunk


class SimData:
    def __init__(self):
        self.foods = []
        self.carriers = []
        self.hosts_alive = []
        self.hosts_dead = []
        self.timestamps = []
        self.parasites = []

    def update(self, plot_data_chunk: SimDataChunk):
        self.foods.append(plot_data_chunk.food)
        self.carriers.append(plot_data_chunk.carriers)
        self.hosts_alive.append(plot_data_chunk.hosts_alive)
        self.hosts_dead.append(plot_data_chunk.hosts_dead)
        self.timestamps.append(plot_data_chunk.timestamp)
        self.parasites.append(plot_data_chunk.parasites)


sim_data = SimData()
