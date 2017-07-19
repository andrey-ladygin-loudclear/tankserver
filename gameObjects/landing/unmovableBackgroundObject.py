from gameObjects.LandingObject import LandingObject


class unmovableBackgroundObject(LandingObject):
    def __init__(self):
        self.type = 'unmovableBackground'