import math
import operator
from time import sleep

import Global

from gameObjects.Tank import Tank
from gameObjects.Wall import Wall


class Game:
    last_id = 0

    def walls(self):

        if len(Global.objects['walls']):
            return Global.objects['walls']

        walls = []

        for i in range(20):
            wall = {
                'id': self.getNextId(),
                'type': 'BrickWall',
                'position': (i*32, 500)
            }
            walls.append(wall)
            cm_wall = Wall()
            cm_wall.id = wall.get('id')
            cm_wall.update_position(wall['position'])

            Global.collision_manager.add(cm_wall) ## ADD TO COLLISIONS

        for i in range(30):
            wall = {
                'id': self.getNextId(),
                'type': 'BrickWall',
                'position': (i*32 + 680, 500)
            }
            walls.append(wall)
            cm_wall = Wall()
            cm_wall.id = wall.get('id')
            cm_wall.update_position(wall['position'])
            Global.collision_manager.add(cm_wall) ## ADD TO COLLISIONS

        Global.objects['walls'] = walls

        return walls

    def callUpdate(self):
        while True:
            self.update()
            sleep(0.05)

    def update(self):
        for bullet in Global.objects['bullets']:
            bullet.update()

        # for player in Global.objects['players']:
        #     player.update()

    def getNextId(self):
        self.last_id += 1
        return self.last_id

    def getPlayerPosition(self):
        return (100, 100)

    def addPlayer(self):
        tank = Tank()
        tank.id = self.getNextId()
        tank.fraction = 'player'
        tank.tankClass = 'KVTank'
        tank.position = self.getPlayerPosition()
        Global.objects['players'].append(tank)

    def getAllObjects(self):
        objects = []

        for player in Global.objects['players']:
            objects.append(player.getObjectFromSelf())

        for bullet in Global.objects['bullets']:
            objects.append(bullet.getObjectFromSelf())

        return objects

