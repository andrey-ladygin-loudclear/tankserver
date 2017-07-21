import math
import random
from threading import Thread, Timer

import time
from cocos import actions
from pyglet.window import key

from gameObjects.Tank import Tank
from gameObjects.bullets.HeavyBullet import HeavyBullet
from gameObjects.bullets.StandartBullet import StandartBullet
from helper import Global


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

            #moving_directions = 0
            #tank_rotate = 1



            #self.increaseSpeed(object.get('mov'))
            #self.setGunRotation(object.get('gun_turn'))
            #self.setTankRotation(object.get('turn'), object.get('mov'))

           # self.addSpeed(moving_directions)
           # self.setPosition(tank_rotate, moving_directions)

            #self.target.move(moving_directions, tank_rotate, 0)
            #self.setGunPosition()

            # Set the object's rotation
            self.check_position()

            time.sleep(0.01)
            #time.sleep(0.5)

    def check_position(self):
        shortest_player, shortest_distanse = self.getPlayerByShortestDistanse()

        if shortest_player and shortest_distanse < 600:
            angleToPlayer = self.getAngleWithPlayer(shortest_player)
            self.rotateGunToPlayer(shortest_player)
            diffAngle = self.getDiffAngleInSector(self.target.getGunRotation(), angleToPlayer)

            #if diffAngle < 10:
            #    self.target.fire()

            if diffAngle < 5:
                self.target.heavy_fire()
        else:
            if self.target.clan == 1:
                self.goto(1100,1600)
            else:
                self.goto(1100,400)


    def goto(self, x, y):
        currx, curry = self.target.position

        if self.getLength(currx, curry, x, y) > 10:
            angle = self.getAngle(currx, curry, x, y)
            self.rotateToAngle(angle)
            self.target.move(1)

    def rotateGunToAngle(self, angle):
        gunAngle = abs(self.target.gun_rotation() % 360)
        angleDiff = self.getDiffAngle(gunAngle, angle)
        self.target.gun_rotation += angleDiff * self.target.rotation_speed

    def rotateToAngle(self, angle):
        tankAngle = abs(self.target.rotation % 360)
        angleDiff = self.getDiffAngle(tankAngle, angle)
        self.target.rotation += angleDiff * self.target.rotation_speed

    def getDiffAngle(self, tankAngle, angle):
        angleDiff = math.floor(tankAngle - angle)

        if angleDiff == -180: angleDiff -= 1

        if (angleDiff > 0 and angleDiff < 180) or angleDiff < -180:
            return -1
        elif (angleDiff < 0 and angleDiff > -180) or angleDiff > 180:
            return 1

        return 0

    def rotateGunToPlayer(self, player):
        angleToPlayer = self.getAngleWithPlayer(player)
        gunAngle = abs(self.target.getGunRotation() % 360)
        angleDiff = gunAngle - angleToPlayer

        if (angleDiff > 0 and angleDiff < 180) or angleDiff < -180:
            self.target.gun_rotation -= 1
        elif (angleDiff < 0 and angleDiff > -180) or angleDiff > 180:
            self.target.gun_rotation += 1

    def getAngleWithPlayer(self, player):
        x1, y1 = self.target.position
        x2, y2 = player.position
        return self.getAngle(x1, y1, x2, y2)

    def getPlayerByShortestDistanse(self):
        shortest_distanse = 0
        shortest_player = None

        for player in Global.GameObjects.getTanks():
            if player.clan == self.target.clan: continue

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

    def getMinDiffAngle(self, angle):
        return min(180 - angle % 180, angle % 180)

    def getDiffAngleInSector(self, angle1, angle2):
        angle1 = self.getMinDiffAngle(angle1)
        angle2 = self.getMinDiffAngle(angle2)
        return abs(angle1 - angle2)

    canHeavyFire = True

    def heavy_fire(self):
        if self.canHeavyFire:
            self.canHeavyFire = False

            bullet = HeavyBullet()
            bullet.rotation = self.target.getGunRotation() - 90 + self.getHeavyGunAngleDeflection()
            bullet.position = self.target.position

            bullet.start_position = bullet.position
            bullet.parent_id = self.target.id
            bullet.id = Global.game.getNextId()
            Global.Queue.append(bullet.getObjectFromSelf())
            Global.GameObjects.addBullet(bullet)

            t = Timer(self.heavyBulletFreezTime, self.acceptHeavyFire)
            t.start()

    canFire = True
    bulletsHolder = 10
    def fire(self):
        if self.canFire:
            self.canFire = False
            self.bulletsHolder -= 1

            bullet = StandartBullet()
            bullet.rotation = self.target.getGunRotation() - 90 + self.getStandartGunAngleDeflection()
            bullet.position = self.target.position
            # bullet.rotation = self.target.Gun.getRotation() + self.target.Gun.getStandartGunAngleDeflection()
            # bullet.position = self.target.Gun.standartFirePosition()

            bullet.start_position = bullet.position
            bullet.parent_id = self.target.id
            bullet.id = Global.game.getNextId()
            Global.Queue.append(bullet.getObjectFromSelf())
            Global.GameObjects.addBullet(bullet)

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