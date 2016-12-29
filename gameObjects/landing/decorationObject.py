
import cocos.collision_model as cm

from gameObjects.LandingObject import LandingObject


class decorationObject(LandingObject):
    def __init__(self):
        #super(decorationObject, self).__init__()
        self.type = 'decoration'
