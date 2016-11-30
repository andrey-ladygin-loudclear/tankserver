import Global
from gameObjects.Tank import Tank


class KVTank(Tank):
    width = 50
    height = 92
    scale = 0.5
    tankClass = ''
    fraction = ''

    def __init__(self):
        self.tankClass = Global.NetworkDataCodes.KVTank
        self.fraction = Global.NetworkDataCodes.PLAYER
