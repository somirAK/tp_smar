import core, utils


class Item:
    def __init__(self):
        self.width = utils.ITEM_WIDTH
        self.position = utils.random_vector2(core.WINDOW_SIZE[0], core.WINDOW_SIZE[1])
        self.color = utils.random_color()

    def show(self):
        core.Draw.circle(self.color, self.position, self.width)


class Obstacle(Item):
    def __init__(self):
        super().__init__()
        self.color = (0, 255, 0)
        self.width = utils.OBSTACLE_WIDTH
        utils.add_exception_position(self.position)


class Creep(Item):
    def __init__(self):
        super().__init__()
