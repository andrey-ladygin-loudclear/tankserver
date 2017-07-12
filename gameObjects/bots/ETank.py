from cocos import sprite

import Global
from gameObjects.Tank import Tank


class BotETank(Tank):
    width = 50
    height = 50
    scale = 0.5
    tankClass = ''
    bot = True

    def __init__(self):
        #super(BotETank, self).__init__('assets/tanks/E-100_1.png')
        self.tankClass = Global.NetworkDataCodes.ETank
        self.fraction = Global.NetworkDataCodes.PLAYER