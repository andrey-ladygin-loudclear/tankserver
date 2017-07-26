from threading import Thread
from time import sleep

from PodSixNet.Server import Server

from events.ClientChannel import ClientChannel
from helper import Global


class Network(Server):
    channelClass = ClientChannel

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)

    def Connected(self, channel, addr):
        print("new connection:", channel)
        ip, port = addr

        Global.PullConnsctions.append(channel)
        index = Global.PullConnsctions.index(channel)

        channel.Send({
            'action': Global.NetworkActions.INIT,
            'connection_index': index
        })

        channel.Send({
            'action': Global.NetworkActions.INIT,
            'walls': Global.game.wallsObjects(),
        })

    def close(self):
        Server.close(self)
        print 'close'

    def sendDataToClients(self, channel):
        print 'sendDataToClients'
        pass
        while True:
            os = Global.game.getAllObjects()
            #print(len(os))
            channel.Send({'action' : Global.NetworkActions.UPDATE, 'objects': os})
            sleep(0.05)