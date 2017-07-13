import random
from time import sleep, time
import cocos.collision_model as cm

import Global
from gameObjects.Collisions import Collisions
from gameObjects.Explosion import Explosion
from gameObjects.Map import Map

from gameObjects.Tank import Tank
from gameObjects.tanks.ETank import ETank
from gameObjects.tanks.KVTank import KVTank
from movingHandlers.BotTankMovingHandlers import BotTankMovingHandlers


class Game:
    last_id = 0
    events = []
    map = Map()

    def wallsObjects(self):
        walls = []
        for wall in self.map.get_walls():
            walls.append(wall.getObjectFromSelf())

        return walls

    def addBot(self):
        tank = ETank()
        tank.id = self.getNextId()
        tank.position = (random.randrange(1, 1000), random.randrange(1, 1000))#random.choice([(500, 500), (1200, 1000), (700, 1500), (1200, 500)])

        moving_handler = BotTankMovingHandlers(tank)
        moving_handler.setDaemon(True)
        moving_handler.start()

        Global.objects['players'].append(tank)
        Global.collision_manager.add(tank)

        self.sendAllTanksToClients()

        return tank.id

    def addPlayer(self):
        tank = KVTank()
        tank.id = self.getNextId()
        tank.position = self.getPlayerPosition()
        Global.objects['players'].append(tank)
        Global.collision_manager.add(tank)
        self.sendAllTanksToClients()
        return tank.id

    def callUpdateBots(self):
        return
        while True:
            self.updateBots()
            sleep(0.033)

    def callUpdatePositions(self):
        while True:
            self.updatePositions()
            sleep(0.033)

    def callCheckCollisions(self):
        while True:
            self.checkCollisions()
            sleep(0.01)

    def updatePositions(self):
        batch = {
            'action': Global.NetworkActions.UPDATE_BATCH,
            'objects': []
        }
        for player in Global.objects['players']:
            player.setNewPosition()
            batch['objects'].append(player.getObjectFromSelf())

            #if player.checkIfStateChanged():
            #Global.Queue.append(player.getObjectFromSelf())
        Global.Queue.append(batch)


    def checkCollisions(self):
        for bullet in Global.objects['bullets']:
            bullet.update()
            bullet.cshape = cm.AARectShape(bullet.position, 2, 2)

            if Collisions.checkWithWalls(bullet) or Collisions.checkWithObjects(bullet, bullet.parent_id) or bullet.exceededTheLengthLimit():
                explosion = Explosion(bullet)
                explosion.checkDamageCollisions()
                bullet.destroy()

        for wall in Global.objects['walls']:
            if wall.health <= 0:
                wall.destroy()


    def updateBots(self):
        pass
    #     for bot in Global.objects['players']:
    #         if bot.bot:
    #             bot


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

    def sendAllTanksToClients(self):
        for player in Global.objects['players']:
            Global.Queue.append(player.getObjectFromSelf())

    def callSendDataToPlayers(self):
        updatePerSecond = 40

        while True:
            data = {
                'action': 'update',
                'data': Global.Queue
            }

            Global.Queue = []

            for channel in Global.PullConnsctions:
                channel.Send(data)

            sleep(1.0/updatePerSecond)


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

