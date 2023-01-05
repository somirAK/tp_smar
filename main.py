import core
import agent as _agent
import item as _item
import utils


def add_random_entities():
    for i in range(utils.NB_AGENTS):
        core.memory(utils.KEY_AGENTS).append(_agent.Agent())
    for i in range(utils.NB_OBSTACLES):
        core.memory(utils.KEY_ITEMS).append(_item.Obstacle())
    for i in range(utils.NB_CREEPS):
        core.memory(utils.KEY_ITEMS).append(_item.Creep())


def setup():
    print("Setup START---------")
    core.fps = 30
    core.WINDOW_SIZE = [800, 600]

    core.memory(utils.KEY_AGENTS, [])
    core.memory(utils.KEY_ITEMS, [])

    add_random_entities()
    print("Setup END-----------")


def compute_perception(agent):
    agent.perception()


def compute_decision(agent):
    agent.decision()


def apply_decision(agent):
    agent.body.move()


def update_environnement(agent):
    for item in core.memory(utils.KEY_ITEMS):
        if agent.can_eat(item):
            if isinstance(item, _item.Obstacle):
                core.memory(utils.KEY_AGENTS).remove(agent)
            if isinstance(item, _item.Creep):
                core.memory(utils.KEY_ITEMS).remove(item)
                agent.body.width += item.width
    # for agent_i in core.memory(utils.KEY_AGENTS):
    #     if agent.can_eat(agent_i):
    #         if agent.body.width > agent_i.body.width:
    #             core.memory(utils.KEY_AGENTS).remove(agent_i)
    #             agent.body.width += agent_i.body.width
    #         else:
    #             core.memory(utils.KEY_AGENTS).remove(agent)
    #             agent_i.body.width += agent.body.width


def run():
    core.cleanScreen()

    for agent in core.memory(utils.KEY_AGENTS):
        agent.show()

    for item in core.memory(utils.KEY_ITEMS):
        item.show()

    for agent in core.memory(utils.KEY_AGENTS):
        compute_perception(agent)

    for agent in core.memory(utils.KEY_AGENTS):
        compute_decision(agent)

    for agent in core.memory(utils.KEY_AGENTS):
        apply_decision(agent)

    for agent in core.memory(utils.KEY_AGENTS):
        update_environnement(agent)


core.main(setup, run)
