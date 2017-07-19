import math
import random

import cocos.collision_model as cm

from gameObjects.Collisions import Collisions
from gameObjects.bullets.HeavyBullet import HeavyBullet

from gameObjects.bullets.StandartBullet import StandartBullet
from helper import Global


class Tank:
    bot = False

    Gun = None
    gun_rotation = 0
    id = 0

    speed = 20

    old_position = (0, 0)
    velocity = (0, 0)

    maxBulletsHolder = 10
    bulletsHolder = 10
    timeForBulletsHolderReload = 3

    #def __init__(self):
        #self.Gun = Gun(self)

    #
    # def _update_position(self):
    #     super(Tank, self)._update_position()
    #     self.Gun.position = self.position
    #     self.Gun.rotation = self.rotation + self.gun_rotation
    #
    #     # self.rotation = 180
    #     # self.Gun.position = self.position
    #     # self.Gun.rotation = self.rotation + self.Gun.gun_rotation


    def heavy_fire(self):
        self.Gun.fireFirstWeapon()

    def fire(self):
        self.Gun.fireSecondWeapon()

    def getObjectFromSelf(self):
        x, y = self.position
        r = self.rotation
        gr = self.gun_rotation

        return {
            'action': Global.NetworkActions.UPDATE,
            Global.NetworkDataCodes.ID: self.id,
            Global.NetworkDataCodes.POSITION: (int(x), int(y)),
            Global.NetworkDataCodes.ROTATION: int(r),
            Global.NetworkDataCodes.GUN_ROTATION: int(gr),
            Global.NetworkDataCodes.FRACTION: self.fraction,
            Global.NetworkDataCodes.TYPE: self.tankClass,
        }

    def getGunRotation(self):
        return self.gun_rotation + self.rotation

    def fire(self, bulletObj):
        if bulletObj.get('type') == Global.NetworkDataCodes.HEAVY_BULLET: bullet = HeavyBullet()
        if bulletObj.get('type') == Global.NetworkDataCodes.STANDART_BULLET: bullet = StandartBullet()

        bullet.position = bulletObj.get('pos')
        bullet.start_position = bullet.position
        bullet.rotation = bulletObj.get('rotation')
        bullet.parent_id = self.id
        bullet.id = Global.game.getNextId()

        Global.Queue.append(bullet.getObjectFromSelf())

        #Global.objects['bullets'].append(bullet)
        Global.GameObjects.addBullet(bullet)


    def damage(self, bullet):
        x, y = self.position
        x2, y2 = bullet.position
        deltax = math.pow(x - x2, 2)
        deltay = math.pow(y - y2, 2)
        delta = (deltax + deltay)
        range = math.sqrt(delta)
        range = range - (self.width + self.height) * self.scale / 2
        #range = max(range / 4, 1)

        #dmg = bullet.damage - math.pow((( -2 * bullet.damageRadius / math.pow(bullet.damageRadius, 2) ) * math.pi * range), 2)
        dmg = bullet.damage * self.damageKoef(range)
        #print('range: ' + str(range))
        #print('damage (without rand): ' + str(dmg))
        dmg += random.randrange(-bullet.damage / 10, bullet.damage / 10)

        self.health -= dmg

        Global.Queue.append({
            "action": Global.NetworkActions.DAMAGE,
            Global.NetworkDataCodes.TYPE: Global.NetworkDataCodes.TANK,
            Global.NetworkDataCodes.ID: self.id,
            Global.NetworkDataCodes.HEALTH: self.health,
            Global.NetworkDataCodes.DAMAGE: dmg
        })

    def damageKoef(self, range):
        maxRange = 20

        try:
            v = math.log(-1 * range + maxRange, 1.22) + 5
        except ValueError:
            v = 0
        return v / maxRange