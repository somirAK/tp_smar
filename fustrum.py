import core
import utils
from pygame.math import Vector2


class CircularFustrum:
    def __init__(self, parent = None):
        self.parent = parent
        self.perception_list = list()  # liste des agents perçus
        self.vision_range = 100  # champ de vision

    def perception(self):
        """
            Parcours tous les objets de l'environnement pour et retourne la
            liste des objets qui sont dans le champ de vision
        """

        self.perception_list.clear()
        for agent in core.memory(utils.KEY_AGENTS):
            if self.inside(agent.body):
                self.perception_list.append(agent)
        return self.perception_list

    def inside(self, obj):
        """
            Permet de savoir si un objet est dans le champ de vision
        """

        if hasattr(obj, "position"):
            if isinstance(obj.position, Vector2):
                if obj.position.distance_to(self.parent.position) < self.vision_range:
                    return True

        return False
