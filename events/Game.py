from time import sleep
import cocos.collision_model as cm

import Global
from gameObjects.Explosion import Explosion

from gameObjects.Tank import Tank
from gameObjects.Wall import Wall


class Game:
    last_id = 0
    events = []

    def walls(self):

        if len(Global.objects['walls']):
            return Global.objects['walls']

        for i in range(20):
            wall = Wall()
            wall.id = self.getNextId()
            wall.type = 'BrickWall'
            wall.position = (i*32, 500)

            wall.cshape = cm.AARectShape(
                wall.position,
                wall.width // 2 - 2,
                wall.height // 2 - 2
            )
            Global.objects['walls'].append(wall)
            Global.collision_manager.add(wall)

        for i in range(30):
            wall = Wall()
            wall.id = self.getNextId()
            wall.type = 'BrickWall'
            wall.position = (i*32 + 680, 500)

            wall.cshape = cm.AARectShape(
                wall.position,
                wall.width // 2 - 2,
                wall.height // 2 - 2
            )
            Global.objects['walls'].append(wall)
            Global.collision_manager.add(wall)

        return Global.objects['walls']

    def wallsObjects(self):
        walls = []
        for wall in self.walls():
            walls.append(wall.getObjectFromSelf())

        return walls

    def callUpdate(self):
        while True:
            self.update()
            sleep(0.05)

    def update(self):
        for bullet in Global.objects['bullets']:
            bullet.update()
            bullet.cshape = cm.AARectShape(
                bullet.position,
                2,
                2
            )
            collisions = Global.collision_manager.objs_colliding(bullet)

            if collisions:
                for wall in Global.objects['walls']:
                    if wall in collisions:
                        #print('EXPLOSION')
                        explosion = Explosion(bullet)
                        explosion.checkDamageCollisions()
                        bullet.destroy()
                        break

        for wall in Global.objects['walls']:
            if wall.health <= 0:
                wall.destroy()

        for channel in Global.Clients:
            os = Global.game.getAllObjects()
            #print(len(os))
            channel.Send({
                'action' : Global.NetworkActions.UPDATE,
                'objects': os,
                'events' : Global.game.getLastEvents()
            })

    def addEvent(self, event):
        self.events.append(event)

    def getLastEvents(self):
        events = self.events
        self.events = []
        return events

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
        #Global.collision_manager.add(tank)

    def getAllObjects(self):
        objects = []

        for player in Global.objects['players']:
            objects.append(player.getObjectFromSelf())

        for bullet in Global.objects['bullets']:
            objects.append(bullet.getObjectFromSelf())

        return objects

