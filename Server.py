from threading import Thread
from time import sleep

import Global
from events.Network import Network

Global.init()
connections_listener = Network(localaddr=(Global.server, 1332))

# myserver.SendToAll({"action": "processSync"}) !!!!!!!!!!!!!!!!!!!!!!!!!

thread = Thread(target = Global.game.callSendPlayers)
thread.setDaemon(True)
thread.start()

while True:
    connections_listener.Pump()
    Global.game.update()
    #sleep(0.0001)
    sleep(0.04)