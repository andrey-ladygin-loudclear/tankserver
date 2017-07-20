from threading import Thread
from time import sleep, time

import cocos.collision_model as cm

#import Global
from events.Game import Game
from events.Network import Network
from helper import Global
from helper.Objects import Objects

connections_listener = Network(localaddr=(Global.server, 1332))

# myserver.SendToAll({"action": "processSync"}) !!!!!!!!!!!!!!!!!!!!!!!!!

Global.CollisionManager = cm.CollisionManagerBruteForce()
Global.game = Game()
Global.GameObjects = Objects()

thread = Thread(target = Global.game.callSendDataToPlayers)
thread.setDaemon(True)
thread.start()


# thread = Thread(target = Global.game.callUpdate, args=(1, ))
# thread.setDaemon(True)
# thread.start()
# thread = Thread(target = Global.game.callUpdate, args=(2, ))
# thread.setDaemon(True)
# thread.start()
# thread = Thread(target = Global.game.callUpdate, args=(3, ))
# thread.setDaemon(True)
# thread.start()

#Global.game.addBot()

thread = Thread(target = Global.game.callUpdatePositions)
thread.setDaemon(True)
thread.start()

thread = Thread(target = Global.game.callCheckCollisions)
thread.setDaemon(True)
thread.start()

# thread = Thread(target = Global.game.callUpdateBots)
# thread.setDaemon(True)
# thread.start()

#Global.game.addBot()
#Global.game.addBot()


def addUnits():
    while True:
        Global.game.addBot(position=(500,400), clan=1)
        Global.game.addBot(position=(1100,400), clan=1)
        Global.game.addBot(position=(1500,400), clan=1)

        Global.game.addBot(position=(800,1600), clan=2)
        Global.game.addBot(position=(1100,1600), clan=2)
        Global.game.addBot(position=(1500,1600), clan=2)
        sleep(60)

thread = Thread(target = addUnits)
thread.setDaemon(True)
thread.start()

Global.game.map.init_walls()

while True:
    connections_listener.Pump()
    sleep(0.0001)
    #t = time()
    #Global.game.update()
    #delta = time() - t
    #sleep_time = max(0.01 - delta, 0.0001)
    #print(sleep_time)
    #sleep(sleep_time)