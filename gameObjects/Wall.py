import math

import Global


class Wall():
    id = 0
    health = 20
    position = (0, 0)
    type = 'wall'

    width = 32
    height = 32
    scale = 1

    def damage(self, bullet):
        x, y = self.position
        x2, y2 = bullet.position
        deltax = math.pow(x - x2, 2)
        deltay = math.pow(y - y2, 2)
        delta = (deltax + deltay) / 3
        range = math.sqrt(max(delta / self.width, 1))
        self.health -= bullet.damage / range

    def destroy(self):
        Global.Queue.append({
            "action": Global.NetworkActions.DESTROY,
            Global.NetworkDataCodes.TYPE: self.type,
            Global.NetworkDataCodes.POSITION: self.position,
            Global.NetworkDataCodes.ID: self.id
        })

        if self in Global.objects['walls']: Global.objects['walls'].remove(self)

    def getObjectFromSelf(self):
        return {
            'action': Global.NetworkActions.UPDATE,
            'id': self.id,
            'position': self.position,
            'type': self.type
        }