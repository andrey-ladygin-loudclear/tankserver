import math
from threading import Thread

import time
from cocos import actions
from pyglet.window import key

import Global


class BotTankMovingHandlers(Thread):

    speed = 0

    rotation_angle = 30

    target = None

    def __init__(self, target):
        Thread.__init__(self)
        self.target = target

    def run(self):
        while True:
            #time.sleep(secondsToSleep)
            #print 'bot moving'
            #print self.target.id, self.target.position

            moving_directions = 1
            tank_rotate = 1



            #self.increaseSpeed(object.get('mov'))
            #self.setGunRotation(object.get('gun_turn'))
            #self.setTankRotation(object.get('turn'), object.get('mov'))

           # self.addSpeed(moving_directions)
           # self.setPosition(tank_rotate, moving_directions)

            self.target.move(moving_directions, tank_rotate, 0)
            #self.setGunPosition()

            # Set the object's rotation
            shortest_player = self.getPlayerByShortestDistanse()

            if shortest_player:
                self.rotateGunToPlayer(shortest_player)

                if self.target.rotation != self.rotation_angle:
                    self.rotateToAngle(self.rotation_angle)

            #self.target.fire()

            #self.target.heavy_fire()
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
            distanse = self.getDistanceByPlayer(player)

            if not shortest_distanse:
                shortest_distanse = distanse
                shortest_player = player

            if distanse < shortest_distanse:
                shortest_distanse = distanse
                shortest_player = player

        return shortest_player

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
