from constants import increment_handlers, SIM_BOARD_SIZE_Y, SIM_BOARD_SIZE_X
from host import Host


class HostMultiplier:
    def __init__(self, display_front, space, foods, hosts):
        self.display_front = display_front
        self.space = space
        self.foods = foods
        self.hosts = hosts

    def multiply_host(self, host):
        offset_y = host.size * 3
        offset_x = host.size * 3
        if host.body.position.y + offset_y >= SIM_BOARD_SIZE_Y:
            offset_y = offset_y * -1
        if host.body.position.x >= SIM_BOARD_SIZE_X:
            offset_x = offset_x * -1

        new_host = Host(self.space, self.display_front, host.body.position.x + offset_x,
                        host.body.position.y + offset_y, increment_handlers(), self.hosts, self, health=80)

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
