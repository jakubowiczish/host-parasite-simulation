class SimDataChunk:
    def __init__(self, food: int, carriers: int, hosts_alive: int, parasites:int, hosts_dead: int, timestamp=float):
        self.food = food
        self.carriers = carriers
        self.hosts_alive = hosts_alive
        self.hosts_dead = hosts_dead
        self.parasites = parasites
        self.timestamp = timestamp

    def __eq__(self, obj):
        return isinstance(obj, SimDataChunk) and obj.food == self.food and obj.carriers == self.carriers \
               and obj.hosts_alive == self.hosts_alive and obj.hosts_dead == self.hosts_dead

    def __ne__(self, other):
        return not self.__eq__(other)