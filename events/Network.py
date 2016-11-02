from threading import Thread
from time import sleep

from PodSixNet.Server import Server

import Global
from events.ClientChannel import ClientChannel


class Network(Server):
    channelClass = ClientChannel

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)

    def Connected(self, channel, addr):
        print("new connection:", channel)
        print('send data to client')

        Global.game.addPlayer()

        thread = Thread(target = self.sendDataToClients, args=(channel,))
        thread.setDaemon(True)
        thread.start()

        channel.Send({'action': Global.NetworkActions.INIT, 'walls': Global.game.walls()})

    def sendDataToClients(self, channel):
        while True:
            #print("send Data To Client")
            channel.Send({'action' : Global.NetworkActions.UPDATE, 'objects': Global.game.getAllObjects()})
            sleep(0.1)