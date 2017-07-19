#from events.Game import Game
#from helper.Objects import Objects

TankNetworkListenerConnection = None

CollisionManager = None
GameObjects = None

PullConnsctions = []
Queue = []

game = None
server = 'localhost'

class NetworkDataCodes:
    TANK_CLASS = 't'
    FRACTION = 'f'
    GUN_ROTATION = 'g'
    POSITION = 'p'
    LAST_UPDATE_TIME = 'lt'
    ROTATION = 'r'
    TYPE = 'y'
    SRC = 's'
    ID = 'i'
    HEALTH = 'h'
    DAMAGE = 'd'
    PARENT_ID = 'pi'

    KVTank = 'k'
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
    UPDATE_BATCH = '8'
