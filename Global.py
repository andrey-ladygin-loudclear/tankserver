from time import sleep

import cocos.collision_model as cm

from events.Game import Game


def init():
    global objects, collision_manager, server, game, PullConnsctions, PullBulletsConnections

    objects = {
        'walls': [],
        'bullets': [],
        'enemies': [],
        'players': [],
    }

    PullConnsctions = []
    PullBulletsConnections = []

    game = Game()
    server = 'localhost'
    collision_manager = cm.CollisionManagerBruteForce()


class NetworkDataCodes:
    TANK_CLASS = 't'
    FRACTION = 'f'
    GUN_ROTATION = 'g'
    POSITION = 'p'
    ROTATION = 'r'
    TYPE = 'y'
    ID = 'i'

    KVTank = 'k'
    PLAYER = 'p'
    TANK = 't'
    BULLET = 'b'

class NetworkActions:
    INIT = '1'
    TANK_MOVE = '2'
    UPDATE = '3'
    TANK_FIRE = '4'
    DESTROY = '5'

