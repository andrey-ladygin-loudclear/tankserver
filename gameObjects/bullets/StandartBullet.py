
import random

import math
from time import time

import Global


class StandartBullet():
    id = 0
    scale = 0.8
    damage = 1
    damageRadius = 5
    fireLength = 1000
    rotation = 0
    position = (0, 0)

    speed = 300

    bullets_fired_offset_x = 6
    bullets_fired_offset_y = 20

    bullets_fired_animation_offset_x = 0
    bullets_fired_animation_offset_y = 5

    def __init__(self):
        self.angle_of_deflection = self.getAngleDeflection()
        self.last_update_time = time()

    def getAngleDeflection(self):
        return random.randrange(-1000, 1000) / 100

    def destroy(self):
        Global.game.addEvent({"action": Global.NetworkActions.DESTROY, "type": "bullet", 'id': self.id})
        if self in Global.objects['bullets']: Global.objects['bullets'].remove(self)

    def update(self):
        angle = self.rotation
        curr_x, curr_y = self.position
        time_delta = (time() - self.last_update_time)
        new_x = self.speed * time_delta * math.cos(math.radians(angle - 180 + self.angle_of_deflection)) + curr_x
        new_y = self.speed * time_delta * math.sin(math.radians(angle + self.angle_of_deflection)) + curr_y
        self.position = (new_x, new_y)
        self.last_update_time = time()

    def getObjectFromSelf(self):
        return {
            Global.NetworkDataCodes.ID: self.id,
            Global.NetworkDataCodes.POSITION: self.position,
            Global.NetworkDataCodes.ROTATION: self.rotation,
            Global.NetworkDataCodes.TYPE: Global.NetworkDataCodes.STANDART_BULLET,
        }