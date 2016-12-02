from PodSixNet.Channel import Channel
from cocos import sprite
import cocos.collision_model as cm
import Global

class EmulatePlayer():
    pass

class ClientChannel(Channel):
    def Network(self, data):
        print(data)

        if data.get('action') == Global.NetworkActions.TANK_MOVE:
            for player in Global.objects['players']:
                if player.id == data.get('id'):
                    player.update(data)
                    break


        if data.get('action') == Global.NetworkActions.TANK_FIRE:
            for player in Global.objects['players']:
                if player.id == data.get('id'):
                    player.fire(data)
                    break

