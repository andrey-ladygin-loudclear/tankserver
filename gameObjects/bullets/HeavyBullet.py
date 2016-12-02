import random

from gameObjects.Bullet import Bullet

import Global

class HeavyBullet(Bullet):

    scale = 1
    damage = 10
    damageRadius = 20
    fireLength = 1000

    speed = 600

    bullets_fired_offset_x = 6
    bullets_fired_offset_y = 20

    bullets_fired_animation_offset_x = 0
    bullets_fired_animation_offset_y = 5

    def __init__(self):
        Bullet.__init__(self)
        self.type = Global.NetworkDataCodes.HEAVY_BULLET
