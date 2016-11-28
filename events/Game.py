from time import sleep, time
import cocos.collision_model as cm

import Global
from gameObjects.Collisions import Collisions
from gameObjects.Explosion import Explosion
from gameObjects.Map import Map

from gameObjects.Tank import Tank
from gameObjects.Wall import Wall


class Game:
    last_id = 0
    events = []
    map = Map()

    def wallsObjects(self):
        walls = []
        for wall in self.map.get_walls():
            walls.append(wall.getObjectFromSelf())

        return walls

    def callUpdate(self, n):
        while True:
            self.update()
            sleep(0.01)

    def update(self):
        for player in Global.objects['players']:
            player.setNewPosition()

        for bullet in Global.objects['bullets']:
            bullet.update()
            bullet.cshape = cm.AARectShape(
                bullet.position,
                2,
                2
            )

            if Collisions.checkWithWalls(bullet):
                explosion = Explosion(bullet)
                explosion.checkDamageCollisions()
                bullet.destroy()

        for wall in Global.objects['walls']:
            if wall.health <= 0:
                wall.destroy()

        for player in Global.objects['players']:
            Global.Queue.append(player.getObjectFromSelf())

    def update_old(self, n):

        bullets_len = len(Global.objects['bullets'])
        for i in range(bullets_len):
            if i+1 == n or (i+1) % n == 0:
                try:
                    bullet = Global.objects['bullets'][i]
                except IndexError:
                    continue

                bullet.update()
                bullet.cshape = cm.AARectShape(
                    bullet.position,
                    2,
                    2
                )
                #Global.Queue.append(bullet.getObjectFromSelf())

                collisions = Global.collision_manager.objs_colliding(bullet)

                if collisions:
                    for wall in Global.objects['walls']:
                        if wall in collisions:
                            print('COLLISION')
                            explosion = Explosion(bullet)
                            explosion.checkDamageCollisions()
                            bullet.destroy()
                            break

        for wall in Global.objects['walls']:
            if wall.health <= 0:
                wall.destroy()

        for player in Global.objects['players']:
            Global.Queue.append(player.getObjectFromSelf())
        return

        #print(time_offset)
        t = time()


        for bullet in Global.objects['bullets']:
            bullet.update()
            bullet.cshape = cm.AARectShape(
                bullet.position,
                2,
                2
            )
            #Global.Queue.append(bullet.getObjectFromSelf())

            collisions = Global.collision_manager.objs_colliding(bullet)

            if collisions:
                for wall in Global.objects['walls']:
                    if wall in collisions:
                        explosion = Explosion(bullet)
                        explosion.checkDamageCollisions()
                        bullet.destroy()
                        break

        for wall in Global.objects['walls']:
            if wall.health <= 0:
                wall.destroy()

        for player in Global.objects['players']:
            Global.Queue.append(player.getObjectFromSelf())

        #print('Update all objects: count: ' + str(len(Global.objects['bullets'])) + ', time: ' + str((time() - t)))

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
        tank.fraction = Global.NetworkDataCodes.PLAYER
        tank.tankClass = Global.NetworkDataCodes.KVTank
        tank.position = self.getPlayerPosition()
        Global.objects['players'].append(tank)

    def callSendDataToPlayers(self):
        while True:
            data = Global.Queue
            Global.Queue = []

            for obj in data:
                for channel in Global.PullConnsctions:
                    channel.Send(obj)

            sleep(0.01)


    # def callSendDataToPlayers(self):
    #     while True:
    #         data = Global.Queue
    #         Global.Queue = []
    #         t = time()
    #
    #         for u in range(100):
    #             data.append({'action': '3', 'i': u+61239, 'r': -138.0, 'y': 'sb', 'p': (450.98192041250684, -130.38067523671657)})
    #
    #         if len(data):
    #             for channel in Global.PullConnsctions:
    #                 channel.Send({
    #                     'action': Global.NetworkActions.UPDATE,
    #                     'o': data
    #                 })
    #             print('count: ' + str(len(data))+', '+str(time() - t))
    #         sleep(0.01)

