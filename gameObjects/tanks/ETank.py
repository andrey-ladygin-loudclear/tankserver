from threading import Timer
import cocos.collision_model as cm

import Global
from objects.Tank import Tank
from objects.bullets.heavyBullet import HeavyBullet
from objects.bullets.standartBullet import StandartBullet


class ETank(Tank):
    width = 50
    height = 50
    scale = 0.5
    tankClass = ''
    fraction = ''

    def __init__(self):
        self.tankClass = Global.NetworkDataCodes.ETank
        self.fraction = Global.NetworkDataCodes.PLAYER