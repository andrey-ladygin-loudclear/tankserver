import math
import random

import cocos.collision_model as cm

import Global
from gameObjects.Collisions import Collisions
from gameObjects.bullets.HeavyBullet import HeavyBullet

from gameObjects.bullets.StandartBullet import StandartBullet


class Tank:
    id = 0
    tankClass = ''
    fraction = ''
    rotation = 0
    gun_rotation = 0
    position = (0, 0)
    prevPosition = (0, 0)
    parent_id = 0

    width = 0
    height = 0
    scale = 1

    health = 100

    # speed = 0
    # speed_acceleration = 0.05
    # max_speed = 1.5
    # rotation_speed = 1.2
    # gun_rotation_speed = 1.2


    speed = 0
    speed_acceleration = 0.1
    max_speed = 1.8
    rotation_speed = 1.2
    gun_rotation_speed = 1.4

    gun_rotation_offset = 0

    client_change_speed = False

    def getObjectFromSelf(self):
        return {
            'action': Global.NetworkActions.UPDATE,
            Global.NetworkDataCodes.ID: self.id,
            Global.NetworkDataCodes.POSITION: self.position,
            Global.NetworkDataCodes.ROTATION: self.rotation,
            Global.NetworkDataCodes.GUN_ROTATION: self.gun_rotation,
            Global.NetworkDataCodes.FRACTION: self.fraction,
            Global.NetworkDataCodes.TYPE: self.tankClass,
        }

    def update(self, object):
        self.move(object.get('mov'), object.get('turn'), object.get('gun_turn'))

    def move(self, move, rotation, gun_rotation):
        self.increaseSpeed(move)
        self.setGunRotation(gun_rotation)
        self.setTankRotation(rotation, move)

    def getNewPosition(self):
        x, y = self.position
        tank_rotation = self.rotation
        cos_x = math.cos(math.radians(tank_rotation + 180))
        sin_x = math.sin(math.radians(tank_rotation + 180))
        return (self.speed * sin_x + x, self.speed * cos_x + y)

    def setNewPosition(self):
        self.prevPosition = self.position
        self.position = self.getNewPosition()
        self.cshape = cm.AARectShape(self.position, self.width//2, self.height//2)

        #if Collisions.checkWithWalls(self):
        if Collisions.checkManualCollisionsWidthWalls(self):
            self.position = self.prevPosition

        self.reduceSpeed()
        self.client_change_speed = False

    def checkIfStateChanged(self):
        return self.position != self.prevPosition

    def reduceSpeed(self):
        if not self.client_change_speed:
            if abs(self.speed - self.speed_acceleration) < self.speed_acceleration:
                self.speed = 0

            if self.speed > 0:
                self.speed = self.speed - self.speed_acceleration
            elif self.speed < 0:
                self.speed = self.speed + self.speed_acceleration

    def increaseSpeed(self, moving_directions):
        if moving_directions:
            self.client_change_speed = True
            speed = self.speed + self.speed_acceleration * moving_directions

            if abs(speed) < self.max_speed:
                self.speed = speed

    def setTankRotation(self, turns_direction, moving_directions):
        self.rotation = self.getTankRotation(turns_direction, moving_directions)

    def getTankRotation(self, turns_direction, moving_directions):
        tank_rotate = self.rotation_speed * turns_direction

        if moving_directions:
            tank_rotate *= moving_directions

        return self.rotation + tank_rotate

    def getPoints(self):
        rotation = abs(self.rotation % 360)

        x, y = self.position
        w, h = (self.width * self.scale, self.height * self.scale)
        cos_x = math.cos(math.radians(rotation))
        sin_x = math.sin(math.radians(rotation))

        x1, y1 = x - w//2, y - h//2
        x2, y2 = x + w//2, y - h//2
        x3, y3 = x + w//2, y + h//2
        x4, y4 = x - w//2, y + h//2

        if rotation > 270:
            x1, y1 = x1 + h//2 * sin_x, y1 - w//2 * cos_x
            x2, y2 = x2 - h//2 * sin_x, y2 - w//2 * cos_x
            x3, y3 = x3 - h//2 * sin_x, y3 + w//2 * cos_x
            x4, y4 = x4 + h//2 * sin_x, y4 + w//2 * cos_x
        elif rotation > 180:
            x1, y1 = x1 + h//2 * sin_x, y1 + w//2 * cos_x
            x2, y2 = x2 - h//2 * sin_x, y2 + w//2 * cos_x
            x3, y3 = x3 - h//2 * sin_x, y3 - w//2 * cos_x
            x4, y4 = x4 + h//2 * sin_x, y4 - w//2 * cos_x
        elif rotation > 90:
            x1, y1 = x1 - h//2 * sin_x, y1 + w//2 * cos_x
            x2, y2 = x2 + h//2 * sin_x, y2 + w//2 * cos_x
            x3, y3 = x3 + h//2 * sin_x, y3 - w//2 * cos_x
            x4, y4 = x4 - h//2 * sin_x, y4 - w//2 * cos_x
        else:
            x1, y1 = x1 - h//2 * sin_x, y1 - w//2 * cos_x
            x2, y2 = x2 + h//2 * sin_x, y2 - w//2 * cos_x
            x3, y3 = x3 + h//2 * sin_x, y3 + w//2 * cos_x
            x4, y4 = x4 - h//2 * sin_x, y4 + w//2 * cos_x

        return ((x1, y1),(x2, y2),(x3, y3),(x4, y4))

    def setGunRotation(self, gun_turns_direction):
        self.gun_rotation_offset += self.gun_rotation_speed * (gun_turns_direction)
        self.gun_rotation = self.rotation + self.gun_rotation_offset

    def fire(self, bulletObj):
        if bulletObj.get('type') == 'HeavyBullet': bullet = HeavyBullet()
        if bulletObj.get('type') == 'StandartBullet': bullet = StandartBullet()

        bullet.position = bulletObj.get('pos')
        bullet.start_position = bullet.position
        bullet.rotation = bulletObj.get('rotation')
        bullet.parent_id = self.id
        bullet.id = Global.game.getNextId()

        Global.Queue.append(bullet.getObjectFromSelf())

        Global.objects['bullets'].append(bullet)


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
        print('range: ' + str(range))
        print('damage (without rand): ' + str(dmg))
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