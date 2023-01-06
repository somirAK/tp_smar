import math

import core
import agent as _agent
import utils
from pygame.math import Vector2


def add_random_entities():
    for i in range(utils.NB_AGENTS_SAINS):
        core.memory(utils.KEY_AGENTS).append(_agent.Agent(utils.SAINS))


def setup():
    print("Setup START---------")
    core.fps = 30
    core.WINDOW_SIZE = [800, 600]

    core.memory(utils.KEY_AGENTS, [])

    add_random_entities()
    print("Setup END-----------")


def compute_perception(agent):
    agent.perception()


def compute_decision(agent):
    if agent.status() != utils.MORT:
        agent.decision()


def apply_decision(agent):
    if agent.status() != utils.MORT:
        agent.body.move()


def update_environnement(agent):
    for agent_i in core.memory(utils.KEY_AGENTS):
        if agent.peut_contaminer(agent_i):
            agent_i.est_contamine()


def update_closest_agent(click_position):
    min_distance = math.inf;
    closest_agent = None

    position = Vector2(click_position[0], click_position[1])

    for agent in core.memory(utils.KEY_AGENTS):
        current_distance = agent.body.position.distance_to(position)
        if current_distance < min_distance:
            min_distance = current_distance
            closest_agent = agent

    closest_agent.est_contamine()


def update_agent_states(agent):
    agent.body.update()


def show_environement_state():
    nb_sains = 0.0
    nb_incube = 0.0
    nb_infecte = 0.0
    nb_retabli = 0.0
    nb_mort = 0.0

    nb_agents = len(core.memory(utils.KEY_AGENTS))

    for agent in core.memory(utils.KEY_AGENTS):
        if agent.body.status == utils.SAINS:
            nb_sains += 1.0
        if agent.body.status == utils.INCUBE:
            nb_incube += 1.0
        if agent.body.status == utils.INFECTE:
            nb_infecte += 1.0
        if agent.body.status == utils.RETABLI:
            nb_retabli += 1.0
        if agent.body.status == utils.MORT:
            nb_mort += 1.0

    print("nb_sains=" + str((nb_sains / nb_agents) * 100) + "%, nb_incube=" + str(
        (nb_incube / nb_agents) * 100) + "%, nb_infecte=" + str((nb_infecte / nb_agents) * 100) + "%, nb_retabli=" + str(
        (nb_retabli / nb_agents) * 100) + "%, nb_mort=" + str((nb_mort / nb_agents) * 100) +"%")


def run():
    core.cleanScreen()

    if core.getMouseLeftClick():
        update_closest_agent(core.getMouseLeftClick())

    for agent in core.memory(utils.KEY_AGENTS):
        agent.show()

    for agent in core.memory(utils.KEY_AGENTS):
        compute_perception(agent)

    for agent in core.memory(utils.KEY_AGENTS):
        compute_decision(agent)

    for agent in core.memory(utils.KEY_AGENTS):
        apply_decision(agent)

    for agent in core.memory(utils.KEY_AGENTS):
        update_environnement(agent)

    for agent in core.memory(utils.KEY_AGENTS):
        update_agent_states(agent)

    show_environement_state()


core.main(setup, run)
