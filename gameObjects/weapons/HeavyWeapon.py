import random

import math
from threading import Timer
from time import time

from gameObjects.bullets.HeavyBullet import HeavyBullet
from helper import Global


class HeavyWeapon:
    heavy_fire_offset_x = -20
    heavy_fire_offset_y = 0
    heavy_fire_animation_offset_x = -35
    heavy_fire_animation_offset_y = 0

    canFire = True
    bulletFreezTime = 3

    gun = None

    def __init__(self, gun):
        self.gun = gun

    def getAngleDeflection(self):
        return random.randrange(-200, 200) / 100

    def firePosition(self):
        cos_x = math.cos(math.radians(self.gun.tank.rotation - 180))
        sin_x = math.sin(math.radians(self.gun.tank.rotation))
        tx, ty = self.gun.tank.position
        x = tx + self.heavy_fire_offset_x * sin_x + self.heavy_fire_offset_y * cos_x
        y = ty - self.heavy_fire_offset_x * cos_x + self.heavy_fire_offset_y * sin_x
        return (x, y)

    def fireRotation(self):
        return self.gun.tank.getGunRotation() - 90 + self.getAngleDeflection()

    def fireAnimationPosition(self):
        cos_x = math.cos(math.radians(self.gun.tank.rotation - 180))
        sin_x = math.sin(math.radians(self.gun.tank.rotation))
        tx, ty = self.gun.tank.position
        x = tx + self.heavy_fire_offset_x * sin_x + self.heavy_fire_offset_y * cos_x
        y = ty - self.heavy_fire_offset_x * cos_x + self.heavy_fire_offset_y * sin_x
        anim_x = x + self.heavy_fire_animation_offset_x * sin_x + self.heavy_fire_animation_offset_y * cos_x
        anim_y = y - self.heavy_fire_animation_offset_x * cos_x + self.heavy_fire_animation_offset_y * sin_x
        return (anim_x, anim_y)

    def acceptFire(self):
        self.canFire = True

    def fire(self, id=None, position=None, rotation=None, last_update_time=None):
        if self.canFire:
            self.canFire = False
            bullet = HeavyBullet()

            if not position: position = self.firePosition()
            if not rotation: rotation = self.fireRotation()
            if not last_update_time: last_update_time = time()

            bullet.id = Global.game.getNextId()
            bullet.parent_id = self.gun.tank.id
            bullet.position = position
            bullet.start_position = position
            bullet.rotation = rotation
            bullet.last_update_time = last_update_time

            Global.Queue.append(bullet.getObjectFromSelf())
            Global.GameObjects.addBullet(bullet)
            t = Timer(self.bulletFreezTime, self.acceptFire)
            t.start()