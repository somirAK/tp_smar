import random
import core
import numpy as np
from pygame.math import Vector2

NB_AGENTS_SAINS = 100
AGENT_WIDTH = 5

KEY_AGENTS = "agents"

SAINS = "sains"
INCUBE = "incube"
INFECTE = "infecte"
RETABLI = "retabli"
MORT = "mort"



COLOR_SAINS = (0,255,0)
COLOR_INCUBE = (0,255,255)
COLOR_INFECTE = (255,0,0)
COLOR_RETABLI = (0,0,255)
COLOR_MORT = (255,255,255)

UUID_EXPETIONS = list()
POSITION_EXCEPTIONS = list()

def random_color():
    return list(np.random.choice(range(256), size=3))


def random_vector2(max_x=core.WINDOW_SIZE[0], max_y=core.WINDOW_SIZE[1]):
    return Vector2(np.random.choice(range(max_x)), np.random.choice(range(max_y)))


def random_uuid():
    uuid = random.randint(1000000, 9999999999)
    while uuid in UUID_EXPETIONS:
        uuid = random.randint(1000000, 9999999999)
    UUID_EXPETIONS.append(uuid)
    return uuid


def add_exception_position(position):
    POSITION_EXCEPTIONS.append(position)
