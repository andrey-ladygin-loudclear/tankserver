
import random

import math


class HeavyBullet():
    id = 0
    scale = 1
    damage = 10
    damageRadius = 20
    position = (0, 0)
    fireLength = 1000
    rotation = 0

    speed = 35

    bullets_fired_offset_x = 6
    bullets_fired_offset_y = 20

    bullets_fired_animation_offset_x = 0
    bullets_fired_animation_offset_y = 5

    def __init__(self):
        self.angle_of_deflection = self.getAngleDeflection()

    def getAngleDeflection(self):
        return random.randrange(-100, 100) / 5

    def update(self):
        angle = self.rotation
        curr_x, curr_y = self.position
        new_x = self.speed * math.cos(math.radians(angle - 180 + self.angle_of_deflection)) + curr_x
        new_y = self.speed * math.sin(math.radians(angle + self.angle_of_deflection)) + curr_y
        self.position = (new_x, new_y)

    def getObjectFromSelf(self):
        return {
            'id': self.id,
            'position': self.position,
            'rotation': self.rotation,
            'typeClass': 'HeavyBullet',
            'type': 'bullet',
        }