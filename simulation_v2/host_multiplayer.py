from constants import increment_handlers
from host import Host


class HostMultiplier:
    def __init__(self, display_front, space, foods, hosts):
        self.display_front = display_front
        self.space = space
        self.foods = foods
        self.hosts = hosts

    def multiply_host(self, host):
        offset = 5
        new_host = Host(self.space, self.display_front, host.body.position.x + offset,
                        host.body.position.y + offset, increment_handlers(), self.hosts, self)

        for other_host in self.hosts:
            handler_host2 = self.space.add_collision_handler(new_host.shape.collision_type,
                                                             other_host.shape.collision_type)
            handler_host2.begin = host.multiply
            other_handler2 = self.space.add_collision_handler(other_host.shape.collision_type,
                                                              new_host.shape.collision_type)
            other_handler2.begin = other_host.multiply
        for food in self.foods:
            handler = self.space.add_collision_handler(new_host.shape.collision_type, food.shape.collision_type)
            handler.data['food'] = food
            handler.data['foods'] = self.foods
            handler.begin = new_host.eat
        self.hosts.append(new_host)
