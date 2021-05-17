class SimDataChunk:
    def __init__(self, food: int, carriers: int, hosts_alive: int, hosts_dead: int, timestamp=float):
        self.food = food
        self.carriers = carriers
        self.hosts_alive = hosts_alive
        self.hosts_dead = hosts_dead
        self.timestamp = timestamp
