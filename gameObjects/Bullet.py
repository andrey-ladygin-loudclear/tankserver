import random

import math
from time import time

from helper import Global


class Bullet():

    id = 0
    parent_id = 0
    damage = 10
    damageRadius = 20
    position = (0, 0)
    start_position = (0, 0)
    rotation = 0
    last_update_time = 0
    type = ''
    fireLength = 600

    speed = 200

    def __init__(self):
        self.last_update_time = time()
        self.fireLength = self.fireLength + random.randrange(-self.fireLength * 0.1, self.fireLength * 0.1)

    def destroy(self):
        Global.Queue.append({
            "action": Global.NetworkActions.DESTROY,
            Global.NetworkDataCodes.TYPE: self.type,
            Global.NetworkDataCodes.POSITION: self.position,
            Global.NetworkDataCodes.ID: self.id
        })

        if self in Global.GameObjects.getBullets(): Global.GameObjects.removeBullet(self)

    def update(self):
        angle = self.rotation
        curr_x, curr_y = self.start_position
        time_delta = (time() - self.last_update_time)
        new_x = self.speed * time_delta * math.cos(math.radians(angle - 180)) + curr_x
        new_y = self.speed * time_delta * math.sin(math.radians(angle)) + curr_y
        self.position = (new_x, new_y)

    def exceededTheLengthLimit(self):
        if self.getLength(self.start_position, self.position) > self.fireLength:
            return True

        return False

    def getLength(self, point1, point2):
        deltax = math.pow(point1[0] - point2[0], 2)
        deltay = math.pow(point1[1] - point2[1], 2)
        return math.sqrt(deltax + deltay)

    def getObjectFromSelf(self):
        return {
            'action': Global.NetworkActions.TANK_FIRE,
            Global.NetworkDataCodes.LAST_UPDATE_TIME: str(self.last_update_time),
            Global.NetworkDataCodes.ID: self.id,
            Global.NetworkDataCodes.PARENT_ID: self.parent_id,
            Global.NetworkDataCodes.POSITION: self.position,
            Global.NetworkDataCodes.ROTATION: self.rotation,
            Global.NetworkDataCodes.TYPE: self.type,
        }