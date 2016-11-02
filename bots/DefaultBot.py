class DefaultBot():
    status = None

    WALK = 1
    ATTACK = 2
    DEFF = 3

    def __init__(self):
        self.status = self.WALK