from threading import Thread
from time import sleep

from PodSixNet.Server import Server

import Global
from events.ClientChannel import ClientChannel

ips = []

class Network(Server):
    channelClass = ClientChannel

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)

    def Connected(self, channel, addr):
        print("new connection:", channel)
        ip, port = addr

        if ip in ips:
            Global.PullConnsctions.append(channel)
        else:
            Global.PullBulletsConnections.append(channel)

        ips.append(ip)

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