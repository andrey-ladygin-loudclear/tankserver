import math

import cocos.collision_model as cm
from cocos.sprite import Sprite

from Landing.LandingObject import LandingObject
from helper import Global


class Center(LandingObject):
    id = 0
    health = 1000
    position = (0, 0)
    width = 135
    height = 141
    scale = .7

    type = 5
    src = ''