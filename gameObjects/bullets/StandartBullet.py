
import random

class StandartBullet():
    id = 0
    scale = 0.8
    damage = 1
    damageRadius = 5
    velocity = (0, 0)
    fireLength = 1000
    rotation = 0
    position = (0, 0)
    moveTo = (0, 0)

    speed = 1

    bullets_fired_offset_x = 6
    bullets_fired_offset_y = 20

    bullets_fired_animation_offset_x = 0
    bullets_fired_animation_offset_y = 5

    def __init__(self):
        self.angle_of_deflection = self.getAngleDeflection()

    def getAngleDeflection(self):
        return random.randrange(-100, 100) / 10

    def getObjectFromSelf(self):
        return {
            'id': self.id,
            'position': self.position,
            'moveTo': self.moveTo,
            'rotation': self.rotation,
            'typeClass': 'StandartBullet',
            'type': 'bullet',
        }