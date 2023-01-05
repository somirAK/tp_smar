from pygame.math import Vector2

import body
import core
import utils
import item as _item


class Agent:
    def __init__(self):
        self.uuid = utils.random_uuid()
        self.body = body.Body()
        self.color = utils.random_color()
        self.perception_list = list()

    def perception(self):
        self.perception_list = self.body.fustrum.perception()

    def filter(self):
        agents = list()
        obstacles = list()
        creeps = list()

        for obj in self.perception_list:
            if isinstance(obj, Agent):
                agents.append(obj)
            if isinstance(obj, _item.Obstacle):
                obstacles.append(obj)
            if isinstance(obj, _item.Creep):
                creeps.append(obj)

        agents.sort(key=lambda a: a.body.position.distance_squared_to(self.body.position), reverse=False)
        creeps.sort(key=lambda c: c.position.distance_squared_to(self.body.position), reverse=False)
        obstacles.sort(key=lambda o: o.position.distance_squared_to(self.body.position), reverse=False)

        return agents, obstacles, creeps

    def decision(self):
        agents, obstacles, creeps = self.filter()
        attraction = Vector2(0, 0)
        repulsion = Vector2(0, 0)

        if len(creeps) == 0:
            return utils.random_vector2(core.WINDOW_SIZE[0], core.WINDOW_SIZE[1])

        attraction_intensity = 2
        for creep in creeps:
            attraction += (creep.position - self.body.position) * attraction_intensity
            attraction_intensity *= 0.05

        for obstacle in obstacles:
            repulsion += self.body.position - obstacle.position

        attraction_intensity = 2
        for agent in agents:
            if agent.body.width > self.body.width:
                repulsion += self.body.position - agent.body.position
            else:
                attraction += (agent.body.position - self.body.position) * attraction_intensity
                attraction_intensity *= 0.05

        if repulsion.length() != 0:
            repulsion.scale_to_length(1/(repulsion.length()**2))

        self.body.acceleration = attraction + repulsion

    def can_eat(self, obj):
        if isinstance(obj, Agent):
            return self.body.position.distance_to(obj.body.position) < self.body.width
        else:
            return self.body.position.distance_to(obj.position) < self.body.width

    def show(self):
        core.Draw.circle(self.color, self.body.position, self.body.width)
