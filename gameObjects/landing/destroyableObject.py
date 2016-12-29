from gameObjects.LandingObject import LandingObject


class destroyableObject(LandingObject):
    def __init__(self):
        #super(destroyableObject, self).__init__()
        self.type = 'destroyable'