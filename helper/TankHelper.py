from gameObjects.tanks.ETank import ETank
from gameObjects.tanks.K1Tank import K1Tank
from gameObjects.tanks.KVTank import KVTank
from gameObjects.tanks.M6Tank import M6Tank
from gameObjects.tanks.Pz2Tank import Pz2Tank
from gameObjects.tanks.PzTank import PzTank
from gameObjects.tanks.T34Tank import T34Tank
from gameObjects.tanks.TigerTank import TigerTank


class TankHelper():

    @staticmethod
    def getSpriteByTank(type):
        if type == 1: return ETank()
        if type == 2: return K1Tank()
        if type == 3: return KVTank()
        if type == 4: return M6Tank()
        if type == 5: return PzTank()
        if type == 6: return Pz2Tank()
        if type == 7: return T34Tank()
        if type == 8: return TigerTank()









