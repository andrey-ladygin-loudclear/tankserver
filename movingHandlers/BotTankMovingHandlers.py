import math
import random
from threading import Thread, Timer

import time
from cocos import actions
from pyglet.window import key

import Global
from gameObjects.Tank import Tank
from gameObjects.bullets.HeavyBullet import HeavyBullet
from gameObjects.bullets.StandartBullet import StandartBullet


class BotTankMovingHandlers(Thread):

    speed = 0

    rotation_angle = 30

    target = None # type: Tank

    def __init__(self, target):
        Thread.__init__(self)
        self.target = target

    def run(self):
        while True:
            #time.sleep(secondsToSleep)
            #print 'bot moving'
            #print self.target.id, self.target.position

            moving_directions = 0
            tank_rotate = 1



            #self.increaseSpeed(object.get('mov'))
            #self.setGunRotation(object.get('gun_turn'))
            #self.setTankRotation(object.get('turn'), object.get('mov'))

           # self.addSpeed(moving_directions)
           # self.setPosition(tank_rotate, moving_directions)

            self.target.move(moving_directions, tank_rotate, 0)
            #self.setGunPosition()

            # Set the object's rotation
            shortest_player, shortest_distanse = self.getPlayerByShortestDistanse()

            if shortest_player:
                angleToPlayer = self.getAngleWithPlayer(shortest_player)
                self.rotateGunToPlayer(shortest_player)

                if self.target.rotation != self.rotation_angle:
                    self.rotateToAngle(self.rotation_angle)

                if shortest_distanse < 800:
                    if abs(self.target.gun_rotation - angleToPlayer) < 10:
                        self.fire()

                    if abs(self.target.gun_rotation - angleToPlayer) < 5:
                        self.heavy_fire()

            time.sleep(0.05)
            #time.sleep(0.5)


    def goto(self, x, y):
        pass

    def rotateToAngle(self, angle):
        tankAngle = abs(self.target.rotation % 360)
        angleDiff = tankAngle - angle

        if (angleDiff > 0 and angleDiff < 180) or angleDiff < -180:
            self.target.rotation -= self.target.rotation_speed
        elif (angleDiff < 0 and angleDiff > -180) or angleDiff > 180:
            self.target.rotation += self.target.rotation_speed

    def rotateGunToPlayer(self, player):
        angleToPlayer = self.getAngleWithPlayer(player)
        gunAngle = abs(self.target.gun_rotation % 360)
        angleDiff = gunAngle - angleToPlayer

        if (angleDiff > 0 and angleDiff < 180) or angleDiff < -180:
            self.target.setGunRotation(-1)
        elif (angleDiff < 0 and angleDiff > -180) or angleDiff > 180:
            self.target.setGunRotation(1)

    def getAngleWithPlayer(self, player):
        x1, y1 = self.target.position
        x2, y2 = player.position
        return self.getAngle(x1, y1, x2, y2)

    def getPlayerByShortestDistanse(self):
        shortest_distanse = 0
        shortest_player = None

        for player in Global.objects['players']:
            if player.bot: continue

            distanse = self.getDistanceByPlayer(player)

            if not shortest_distanse:
                shortest_distanse = distanse
                shortest_player = player

            if distanse < shortest_distanse:
                shortest_distanse = distanse
                shortest_player = player

        return shortest_player, shortest_distanse

    def getDistanceByPlayer(self, player):
        x1, y1 = self.target.position
        x2, y2 = player.position
        return self.getLength(x1, y1, x2, y2)


    def getLength(self, x1, y1, x2, y2):
        deltax = math.pow(x1 - x2, 2)
        deltay = math.pow(y1 - y2, 2)
        return math.sqrt(deltax + deltay)

    def getAngle(self, x1, y1, x2, y2):
        deltaX = x2 - x1
        deltaY = y2 - y1
        rad = math.atan2(deltaX, deltaY)
        return rad * (180 / math.pi) + 180
        if degrees < 0: degrees += 360
        return degrees

    canHeavyFire = True

    def heavy_fire(self):
        if self.canHeavyFire:
            self.canHeavyFire = False

            bullet = HeavyBullet()
            bullet.rotation = self.target.gun_rotation - 90 + self.getHeavyGunAngleDeflection()
            bullet.position = self.target.position

            bullet.start_position = bullet.position
            bullet.parent_id = self.target.id
            bullet.id = Global.game.getNextId()
            Global.Queue.append(bullet.getObjectFromSelf())
            Global.objects['bullets'].append(bullet)

            t = Timer(self.heavyBulletFreezTime, self.acceptHeavyFire)
            t.start()

    canFire = True
    bulletsHolder = 10
    def fire(self):
        if self.canFire:
            self.canFire = False
            self.bulletsHolder -= 1

            bullet = StandartBullet()
            bullet.rotation = self.target.gun_rotation - 90 + self.getStandartGunAngleDeflection()
            bullet.position = self.target.position
            # bullet.rotation = self.target.Gun.getRotation() + self.target.Gun.getStandartGunAngleDeflection()
            # bullet.position = self.target.Gun.standartFirePosition()

            bullet.start_position = bullet.position
            bullet.parent_id = self.target.id
            bullet.id = Global.game.getNextId()
            Global.Queue.append(bullet.getObjectFromSelf())
            Global.objects['bullets'].append(bullet)

            if not self.bulletsHolder:
                t = Timer(3, self.bulletsHolderReload)
                t.start()
                return

            t = Timer(self.bulletFreezTime, self.acceptFire)
            t.start()

    bulletFreezTime = 0.1
    heavyBulletFreezTime = 3

    def bulletsHolderReload(self):
        self.canFire = True
        self.bulletsHolder = 10

    def acceptFire(self):
        self.canFire = True

    def acceptHeavyFire(self):
        self.canHeavyFire = True


    def getHeavyGunAngleDeflection(self):
        return random.randrange(-200, 200) / 100

    def getStandartGunAngleDeflection(self):
        return random.randrange(-500, 500) / 100