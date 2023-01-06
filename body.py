import random

from pygame.math import Vector2

import core
import epidemie
import fustrum as _fustrum
import utils


class Body:
    def __init__(self, status=utils.SAINS):
        self.fustrum = _fustrum.CircularFustrum(parent=self)
        self.width = utils.AGENT_WIDTH
        self.position = utils.random_vector2(core.WINDOW_SIZE[0], core.WINDOW_SIZE[1])
        self.vitesse = utils.random_vector2(10, 10)
        self.vitesse_max = 20
        self.acceleration = Vector2()
        self.acceleration_max = 50

        self.status = status

        self.peut_contaminer = False
        self.duree_incubation = 0
        self.duree_contagion = 0
        self.duree_deces = 0

    def move(self):
        """
            Change la position du body selon son acceleration et sa vitesse
        """

        if self.status == utils.MORT:
            self.vitesse = Vector2(0,0)
            self.acceleration = Vector2(0,0)
            return

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

    def update(self):
        if self.status == utils.INCUBE:
            self.duree_incubation += 1
            if self.duree_incubation > epidemie.DUREE_INCUBATION:
                self.status = utils.INFECTE
                self.duree_contagion = 0

        if self.status == utils.INFECTE:
            self.duree_contagion += 1
            self.duree_deces += 1

            if self.duree_contagion > epidemie.DUREE_AVANT_CONTAGION:
                self.peut_contaminer = True

            if self.duree_deces > epidemie.DUREE_AVANT_DECES:
                if random.random() < epidemie.POURCENTAGE_MORTALITE:
                    self.status = utils.MORT
                else:
                    self.status = utils.RETABLI
