from time import sleep

from PodSixNet.Channel import Channel

from helper import Global


class ClientChannel(Channel):
    def Network(self, data):
        #print(data)
        #sleep(.02)

        for player in Global.GameObjects.getTanks():
            if player.id == data.get('id'):

                if data.get('action') == Global.NetworkActions.TANK_MOVE:
                    player.update(data)

                if data.get('action') == Global.NetworkActions.TANK_FIRE:
                    player.fire(data)

