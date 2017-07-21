import math
import random

import cocos.collision_model as cm

from gameObjects.Collisions import Collisions
from gameObjects.Gun import Gun
from gameObjects.bullets.HeavyBullet import HeavyBullet

from gameObjects.bullets.StandartBullet import StandartBullet
from helper import Global


class Tank:
    bot = False
    clan = 0

    Gun = None
    id = 0

    old_position = (0, 0)
    velocity = (0, 0)

    maxBulletsHolder = 10
    bulletsHolder = 10
    timeForBulletsHolderReload = 3

    width = 50
    height = 50
    scale = 0.5

    health = 100

    gun_rotation = 0
    rotation = 0
    rotation_speed = 1
    gun_rotation_speed = 1
    speed = 2


    def __init__(self):
        self.Gun = Gun(self)

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
            Global.NetworkDataCodes.TYPE: self.clan,
            Global.NetworkDataCodes.HEALTH: self.health,
        }

    def getGunRotation(self):
        return self.gun_rotation + self.rotation

    def setPosition(self, position):
        self.position = position
        self.cshape = cm.AARectShape(self.position, self.width//2, self.height//2)

    def move(self, speed):
        x, y = self.position
        tank_rotation = self.rotation
        cos_x = math.cos(math.radians(tank_rotation + 180))
        sin_x = math.sin(math.radians(tank_rotation + 180))
        new_position = (speed * sin_x + x, speed * cos_x + y)

        obj = Tank()
        obj.setPosition(new_position)
        obj.cshape = cm.AARectShape(obj.position, obj.width//2, obj.height//2)

        #if Collisions.checkManualCollisionsWidthWalls(self):
        # collisions = Global.CollisionManager.objs_colliding(obj)
        # if Global.CollisionManager.knows(obj):
        #     Global.CollisionManager.remove_tricky(obj)
        #
        # if obj in collisions:
        #     return

        self.setPosition(obj.position)
        del obj

    def update(self, data):
        self.position = data.get('position')
        self.gun_rotation = data.get('gun_rotation')
        self.rotation = data.get('rotation')

    # def fire(self, bulletObj):
    #     if bulletObj.get('type') == Global.NetworkDataCodes.HEAVY_BULLET: bullet = HeavyBullet()
    #     if bulletObj.get('type') == Global.NetworkDataCodes.STANDART_BULLET: bullet = StandartBullet()
    #
    #     bullet.position = bulletObj.get('pos')
    #     bullet.start_position = bullet.position
    #     bullet.rotation = bulletObj.get('rotation')
    #     bullet.parent_id = self.id
    #     bullet.id = Global.game.getNextId()
    #
    #     Global.Queue.append(bullet.getObjectFromSelf())
    #
    #     #Global.objects['bullets'].append(bullet)
    #     Global.GameObjects.addBullet(bullet)


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

    def destroy(self):
        Global.Queue.append({
            "action": Global.NetworkActions.DESTROY,
            Global.NetworkDataCodes.TYPE: Global.NetworkDataCodes.TANK,
            Global.NetworkDataCodes.POSITION: self.position,
            Global.NetworkDataCodes.ID: self.id
        })

        if self in Global.GameObjects.getTanks(): Global.GameObjects.removeTank(self)

    def damageKoef(self, range):
        maxRange = 20

        try:
            v = math.log(-1 * range + maxRange, 1.22) + 5
        except ValueError:
            v = 0
        return v / maxRange