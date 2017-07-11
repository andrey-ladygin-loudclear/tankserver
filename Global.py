from time import sleep

import cocos.collision_model as cm

from events.Game import Game


def init():
    global objects, collision_manager, server, game, PullConnsctions, PullBulletsConnections, Queue

    objects = {
        'walls': [],
        'bullets': [],
        'enemies': [],
        'players': [],
    }

    PullConnsctions = []
    PullBulletsConnections = []

    Queue = []

    game = Game()
    server = 'localhost'
    collision_manager = cm.CollisionManagerBruteForce()


class NetworkDataCodes:
    TANK_CLASS = 't'
    FRACTION = 'f'
    GUN_ROTATION = 'g'
    POSITION = 'p'
    LAST_UPDATE_TIME = 'lt'
    ANGLE_OF_DEFLECTION = 'aod'
    ROTATION = 'r'
    TYPE = 'y'
    SRC = 's'
    ID = 'i'
    HEALTH = 'h'
    DAMAGE = 'd'
    PARENT_ID = 'pi'

    KVTank = 'k'
    ETank = 'e'
    PLAYER = 'p'
    TANK = 't'
    BULLET = 'b'
    STANDART_BULLET = 'sb'
    HEAVY_BULLET = 'hb'
    WALL = 'w'


class NetworkActions:
    INIT = '1'
    TANK_MOVE = '2'
    UPDATE = '3'
    TANK_FIRE = '4'
    DESTROY = '5'
    TEST = '6'
    DAMAGE = '7'

