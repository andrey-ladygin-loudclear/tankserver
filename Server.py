from threading import Thread
from time import sleep, time

import Global
from events.Network import Network

Global.init()
connections_listener = Network(localaddr=(Global.server, 1332))

# myserver.SendToAll({"action": "processSync"}) !!!!!!!!!!!!!!!!!!!!!!!!!

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

thread = Thread(target = Global.game.callUpdate, args=(3, ))
thread.setDaemon(True)
thread.start()

while True:
    connections_listener.Pump()
    sleep(0.0001)
    #t = time()
    #Global.game.update()
    #delta = time() - t
    #sleep_time = max(0.01 - delta, 0.0001)
    #print(sleep_time)
    #sleep(sleep_time)