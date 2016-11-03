import math

import Global
from gameObjects.bullets.HeavyBullet import HeavyBullet

from gameObjects.bullets.StandartBullet import StandartBullet


class Tank:
    id = 0
    tankClass = ''
    fraction = ''
    rotation = 0
    gun_rotation = 0
    position = (0, 0)
    parent_id = 0

    speed = 0
    speed_acceleration = 0.2
    max_speed = 3
    rotation_speed = 1.2
    gun_rotation_speed = 1.2

    gun_rotation_offset = 0

    def getObjectFromSelf(self):
        return {
            'id': self.id,
            'position': self.position,
            'rotation': self.rotation,
            'gun_rotation': self.gun_rotation,
            'fraction': self.fraction,
            'tankClass': self.tankClass,
            'type': 'tank',
        }

    def update(self, object):
        self.addSpeed(object.get('mov'))
        self.setGunRotation(object.get('gun_turn'))
        self.setTankRotation(object.get('turn'), object.get('mov'))
        self.setNewPosition()

    def setNewPosition(self):
        x, y = self.position
        tank_rotation = self.rotation
        cos_x = math.cos(math.radians(tank_rotation + 180))
        sin_x = math.sin(math.radians(tank_rotation + 180))
        self.position = (self.speed * sin_x + x, self.speed * cos_x + y)

    def addSpeed(self, moving_directions):
        if moving_directions:
            speed = self.speed + self.speed_acceleration * moving_directions

            if abs(speed) < self.max_speed:
                self.speed = speed

        else:
            if self.speed > 0:
                self.speed -= self.speed_acceleration
            elif self.speed < 0:
                self.speed += self.speed_acceleration

    def setTankRotation(self, turns_direction, moving_directions):
        self.rotation = self.getTankRotation(turns_direction, moving_directions)

    def getTankRotation(self, turns_direction, moving_directions):
        tank_rotate = self.rotation_speed * turns_direction

        if moving_directions:
            tank_rotate *= moving_directions

        return self.rotation + tank_rotate

    def setGunRotation(self, gun_turns_direction):
        self.gun_rotation_offset += self.gun_rotation_speed * (gun_turns_direction)
        self.gun_rotation = self.rotation + self.gun_rotation_offset

    def fire(self, bulletObj):

        if bulletObj.get('type') == 'HeavyBullet': bullet = HeavyBullet()
        if bulletObj.get('type') == 'StandartBullet': bullet = StandartBullet()

        bullet.position = bulletObj.get('pos')
        bullet.rotation = bulletObj.get('rotation')
        bullet.parent_id = self.id
        bullet.id = Global.game.getNextId()

        Global.objects['bullets'].append(bullet)