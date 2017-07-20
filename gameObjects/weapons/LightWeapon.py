import random

import math
from threading import Timer
from time import time

from gameObjects.bullets.StandartBullet import StandartBullet
from helper import Global


class LightWeapon:
    standart_fire_offset_x = -20
    standart_fire_offset_y = 5
    standart_fire_animation_offset_x = -5
    standart_fire_animation_offset_y = 0

    canFire = True
    bulletsHolder = 10
    bulletFreezTime = 0.1
    heavyBulletFreezTime = 3

    gun = None

    def __init__(self, gun):
        self.gun = gun

    def getAngleDeflection(self):
        return random.randrange(-500, 500) / 100

    def firePosition(self):
        cos_x = math.cos(math.radians(self.gun.tank.rotation - 180))
        sin_x = math.sin(math.radians(self.gun.tank.rotation))
        tx, ty = self.gun.tank.position
        x = tx + self.standart_fire_offset_x * sin_x + self.standart_fire_offset_y * cos_x
        y = ty - self.standart_fire_offset_x * cos_x + self.standart_fire_offset_y * sin_x
        return (x, y)

    def fireRotation(self):
        return self.gun.tank.getGunRotation() - 90 + self.getAngleDeflection()

    def fireAnimationPosition(self):
        cos_x = math.cos(math.radians(self.gun.tank.rotation - 180))
        sin_x = math.sin(math.radians(self.gun.tank.rotation))
        tx, ty = self.gun.tank.position
        x = tx + self.standart_fire_offset_x * sin_x + self.standart_fire_offset_y * cos_x
        y = ty - self.standart_fire_offset_x * cos_x + self.standart_fire_offset_y * sin_x
        anim_x = x + self.standart_fire_animation_offset_x * sin_x + self.standart_fire_animation_offset_y * cos_x
        anim_y = y - self.standart_fire_animation_offset_x * cos_x + self.standart_fire_animation_offset_y * sin_x
        return (anim_x, anim_y)

    def fire(self, id=None, position=None, rotation=None, last_update_time=None):
        if self.canFire:
            self.canFire = False
            self.bulletsHolder -= 1
            bullet = StandartBullet()

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

            if not self.bulletsHolder:
                t = Timer(3, self.bulletsHolderReload)
                t.start()
                return

            t = Timer(self.bulletFreezTime, self.acceptFire)
            t.start()

    def bulletsHolderReload(self):
        self.canFire = True
        self.bulletsHolder = 10

    def acceptFire(self):
        self.canFire = True