from time import sleep

from PodSixNet.Channel import Channel

from helper import Global


class ClientChannel(Channel):
    def Network(self, data):
        #print data

        if data.get('action') == Global.NetworkActions.INIT:
            index = int(data.get('connection_index'))
            type = data.get('type')
            channel = Global.PullConnsctions[index]
            id = Global.game.addPlayer(type)
            channel.Send({
                'action': Global.NetworkActions.INIT,
                'id': id
            })

        for player in Global.GameObjects.getTanks():
            if player.id == data.get('id'):

                if data.get('action') == Global.NetworkActions.TANK_MOVE:
                    player.update(data)

                if data.get('action') == Global.NetworkActions.TANK_FIRE:
                    if data.get('type') == Global.NetworkDataCodes.HEAVY_BULLET:
                        player.heavy_fire()

                    if data.get('type') == Global.NetworkDataCodes.STANDART_BULLET:
                        player.fire()

