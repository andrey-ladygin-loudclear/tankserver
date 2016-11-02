import cocos.collision_model as cm

from events.Game import Game


def init():
    global objects, collision_manager, server, game

    objects = {
        'walls': [],
        'bullets': [],
        'enemies': [],
        'players': [],
    }

    game = Game()
    server = 'localhost'
    collision_manager = cm.CollisionManagerBruteForce()

class NetworkActions:
    INIT = '1'
    TANK_MOVE = '2'
    UPDATE = '3'
    TANK_FIRE = '4'