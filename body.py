from pygame.math import Vector2

import core
import fustrum as _fustrum
import utils


class Body:
    def __init__(self):
        self.fustrum = _fustrum.CircularFustrum(parent=self)
        self.width = utils.AGENT_WIDTH
        self.position = utils.random_vector2(core.WINDOW_SIZE[0], core.WINDOW_SIZE[1])
        self.vitesse = utils.random_vector2(10, 10)
        self.vitesse_max = 20
        self.acceleration = Vector2()
        self.acceleration_max = 50

    def move(self):
        """
            Change la position du body selon son acceleration et sa vitesse
        """

        if self.acceleration.length() > self.acceleration_max:
            self.acceleration.scale_to_length(self.acceleration_max)

        self.vitesse += self.acceleration

        if self.vitesse.length() > self.vitesse_max:
            self.vitesse.scale_to_length(self.vitesse_max)

        destination = self.position + self.vitesse

        if destination.x > core.WINDOW_SIZE[0] or destination.x < 0:
            self.vitesse.x *= -1
            self.acceleration.x *= -1
        if destination.y > core.WINDOW_SIZE[1] or destination.y < 0:
            self.vitesse.y *= -1
            self.acceleration.y *= -1

        self.position += self.vitesse
