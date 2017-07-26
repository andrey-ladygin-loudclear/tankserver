from gameObjects.Tank import Tank


class PzTank(Tank):

    type = 5

    def __init__(self):
        Tank.__init__(self)
