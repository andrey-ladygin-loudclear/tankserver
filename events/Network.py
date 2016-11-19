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
        ip, port = addr

        Global.PullConnsctions.append(channel)

        Global.game.addPlayer()

        # thread = Thread(target = self.sendDataToClients, args=(channel,))
        # thread.setDaemon(True)
        # thread.start()

        channel.Send({
            'action': Global.NetworkActions.INIT,
            'walls': Global.game.wallsObjects(),
            #'id': channel.id
        })

    def sendDataToClients(self, channel):
        pass
        while True:
            os = Global.game.getAllObjects()
            #print(len(os))
            channel.Send({'action' : Global.NetworkActions.UPDATE, 'objects': os})
            sleep(0.05)