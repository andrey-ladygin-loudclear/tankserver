import math
from cocos import actions
from pyglet.window import key

import Global


class BotTankMovingHandlersOLD(actions.Move):

    speed = 0

    rotation_angle = 30

    def __init__(self):
        super(BotTankMovingHandlers, self).__init__()
        #self.Bot = DefaultBot()

    # step() is called every frame.
    # dt is the number of seconds elapsed since the last call.
    def step(self, dt):
        super(BotTankMovingHandlers, self).step(dt) # Run step function on the parent class.

        print 'bot moving'

        moving_directions = 0
        tank_rotate = 0

        self.addSpeed(moving_directions)
        self.setPosition(tank_rotate, moving_directions)
        self.setGunPosition()

        # Set the object's rotation
        shortest_player = self.getPlayerByShortestDistanse()
        self.rotateGunToPlayer(shortest_player)

        if self.target.rotation != self.rotation_angle:
            self.rotateToAngle(self.rotation_angle)

        #self.target.fire()

        #self.target.heavy_fire()

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
        gunAngle = abs(self.target.Gun.rotation % 360)
        angleDiff = gunAngle - angleToPlayer

        if (angleDiff > 0 and angleDiff < 180) or angleDiff < -180:
            self.setGunRotation(-1)
        elif (angleDiff < 0 and angleDiff > -180) or angleDiff > 180:
            self.setGunRotation(1)

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
        deltaX = x2 - x1qq
        deltaY = y2 - y1
        rad = math.atan2(deltaX, deltaY)
        return rad * (180 / math.pi) + 180
        if degrees < 0: degrees += 360
        return degrees


    def setPosition(self, turns_direction, moving_directions):
        tank_rotate = self.target.rotation_speed * turns_direction

        if moving_directions:
            tank_rotate *= moving_directions

        tank_rotate += self.target.rotation
        self.target.rotation = tank_rotate

        cos_x = math.cos(math.radians(tank_rotate + 180))
        sin_x = math.sin(math.radians(tank_rotate + 180))
        self.target.velocity = (self.speed * sin_x, self.speed * cos_x)

    def setGunPosition(self):
        self.target.Gun.position = self.target.position

    def setGunRotation(self, gun_turns_direction):
        self.target.Gun.gun_rotation += self.target.gun_rotation_speed * (gun_turns_direction)
        self.target.Gun.rotation = self.target.rotation + self.target.Gun.gun_rotation

    def addSpeed(self, moving_directions):
        if moving_directions:
            speed = self.speed + self.target.speed_acceleration * moving_directions

            if abs(speed) < self.target.max_speed:
                self.speed = speed

        else:
            if self.speed > 0:
                self.speed -= self.target.speed_acceleration
            elif self.speed < 0:
                self.speed += self.target.speed_acceleration