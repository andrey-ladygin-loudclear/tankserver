
import random

from gameObjects.Bullet import Bullet
from helper import Global


class StandartBullet(Bullet):

    scale = 0.8
    damage = 2
    damageRadius = 5
    fireLength = 400

    speed = 400

    bullets_fired_offset_x = 6
    bullets_fired_offset_y = 20

    bullets_fired_animation_offset_x = 0
    bullets_fired_animation_offset_y = 5

    def __init__(self):
        Bullet.__init__(self)
        self.type = Global.NetworkDataCodes.STANDART_BULLET
