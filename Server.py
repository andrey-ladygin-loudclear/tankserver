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
        # Global.game.addBot(position=(500,450), clan=1, rotation=180, type=1)
        # Global.game.addBot(position=(600,450), clan=1, rotation=180, type=2)
        # Global.game.addBot(position=(700,450), clan=1, rotation=180, type=3)
        # Global.game.addBot(position=(800,450), clan=1, rotation=180, type=4)
        # Global.game.addBot(position=(900,450), clan=1, rotation=180, type=5)
        # Global.game.addBot(position=(1000,450), clan=1, rotation=180, type=6)
        # Global.game.addBot(position=(1100,450), clan=1, rotation=180, type=7)

        #Global.game.addBot(position=(800,3870 - 350), clan=2, type=2)
        #Global.game.addBot(position=(1100,3870 - 350), clan=2, type=2)
        #Global.game.addBot(position=(1500,3870 - 350), clan=2, type=2)

        #Global.game.addBot(position=(800,600), clan=2, type=2)
        #Global.game.addBot(position=(1100,600), clan=2, type=2)
        Global.game.addBot(position=(800,600), clan=2, type=2)

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