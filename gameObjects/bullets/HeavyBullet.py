
import random

import math
from time import time

import Global


class HeavyBullet():
    id = 0
    scale = 1
    damage = 10
    damageRadius = 20
    position = (0, 0)
    fireLength = 1000
    rotation = 0

    speed = 200

    bullets_fired_offset_x = 6
    bullets_fired_offset_y = 20

    bullets_fired_animation_offset_x = 0
    bullets_fired_animation_offset_y = 5

    def __init__(self):
        self.angle_of_deflection = self.getAngleDeflection()
        self.last_update_time = time()

    def getAngleDeflection(self):
        return random.randrange(-1000, 1000) / 50

    def destroy(self):
        for channel in Global.Clients:
            channel.Send({"action": Global.NetworkActions.DESTROY, "type": "bullet", 'id': self.id})

        if self in Global.objects['bullets']: Global.objects['bullets'].remove(self)

    def update(self):
        angle = self.rotation
        curr_x, curr_y = self.position
        time_delta = (time() - self.last_update_time)
        new_x = self.speed * time_delta * math.cos(math.radians(angle - 180 + self.angle_of_deflection)) + curr_x
        new_y = self.speed * time_delta * math.sin(math.radians(angle + self.angle_of_deflection)) + curr_y
        self.position = (new_x, new_y)

    def getObjectFromSelf(self):
        return {
            Global.NetworkDataCodes.ID: self.id,
            Global.NetworkDataCodes.POSITION: self.position,
            Global.NetworkDataCodes.ROTATION: self.rotation,
            Global.NetworkDataCodes.TYPE: Global.NetworkDataCodes.HEAVY_BULLET,
        }