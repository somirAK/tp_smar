import random

from pygame.math import Vector2

import body
import core
import epidemie
import utils


class Agent:
    def __init__(self, status=utils.SAINS):
        self.uuid = utils.random_uuid()
        self.body = body.Body(status)
        self.perception_list = list()

        self.separationFactor=1
        self.alignFactor = 0.1
        self.cohesionFactor = 1
        self.se=Vector2()
        self.co = Vector2()

    def perception(self):
        """
            Récupère la liste des éléments perçus par le fustrum
        """

        self.perception_list = self.body.fustrum.perception()

    def status(self):
        return self.body.status

    def decision(self):
        """
            Récupère les éléments de sa perception et ajoute une attraction ou une répulsion
            selon la nature de l'objet perçu.
            L'attraction et la répulsion est ensuite ajouté a l'accéleration du body
        """

        if self.status() != utils.MORT:
            self.body.acceleration = Vector2(random.uniform(-5, 5), random.uniform(-5, 5))

    def peut_contaminer(self, obj):

        if isinstance(obj, Agent):
            return self.body.position.distance_to(
                obj.body.position) < epidemie.DISTANCE_MINI_CONTAGION and self.body.peut_contaminer and random.random() < epidemie.POURCENTAGE_CONTAGION
        else:
            return False

    def est_contamine(self):
        self.body.status = utils.INCUBE

    def show(self):
        if self.status() == utils.SAINS:
            core.Draw.circle(utils.COLOR_SAINS, self.body.position, self.body.width)
        elif self.status() == utils.INCUBE:
            core.Draw.circle(utils.COLOR_INCUBE, self.body.position, self.body.width)
        elif self.status() == utils.INFECTE:
            core.Draw.circle(utils.COLOR_INFECTE, self.body.position, self.body.width)
        elif self.status() == utils.RETABLI:
            core.Draw.circle(utils.COLOR_RETABLI, self.body.position, self.body.width)
        elif self.status() == utils.MORT:
            core.Draw.circle(utils.COLOR_MORT, self.body.position, self.body.width)

    def flock(self, agents):
        perception = self.perception_list

        self.co = self.cohesion(perception) * self.cohesionFactor
        al = self.align(perception) * self.alignFactor
        self.se = self.separation(perception) * -self.separationFactor

        self.acceleration += self.se + self.co + al
        
    
    def separation(self,agents):
        steering = Vector2()
        agentscounter = 0
        for other in agents:
            if self.position.distance_to(other.position) != 0:
                diff = Vector2(other.position.x-self.position.x,other.position.y-self.position.y)
                if diff.length() > 0.001:
                    diff.scale_to_length(self.position.distance_squared_to(other.position))
                    agentscounter += 1
                    steering += diff
            else:
                steering += Vector2(random.uniform(-5,5),random.uniform(-5,5))
                agentscounter += 1

        if agentscounter > 0:
            steering /= agentscounter

            steering += self.vitesse

            if steering.length() > self.maxAcc:
                steering = steering.normalize()
                steering.scale_to_length(self.maxAcc)
        return steering

    def cohesion(self,agents):
        steering = Vector2()
        agentscounter = 0
        for other in agents:
            if self.position.distance_to(other.position) != 0:
                agentscounter += 1
                steering += other.position

        if agentscounter > 0:
            steering /= agentscounter
            steering -= self.position


            steering += self.vitesse
            if steering.length() > self.maxAcc:
                steering = steering.normalize()
                steering.scale_to_length(self.maxAcc)

        return steering

    def align(self, agents):
        steering = Vector2()
        agentscounter = 0
        for other in agents:
            agentscounter+=1
            steering+=other.vitesse

        if agentscounter>0:
            steering/=agentscounter

            steering -= self.vitesse
            if steering.length() > self.maxAcc:
                steering=steering.normalize()
                steering.scale_to_length(self.maxAcc)

        return steering
