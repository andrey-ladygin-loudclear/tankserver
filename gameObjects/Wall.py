import math

import Global


class Wall():
    id = 0
    health = 20
    position = (0, 0)
    type = ''

    width = 32
    height = 32

    def damage(self, bullet):
        x, y = self.position
        x2, y2 = bullet.position
        deltax = math.pow(x - x2, 2)
        deltay = math.pow(y - y2, 2)
        delta = (deltax + deltay) / 3
        range = math.sqrt(max(delta / self.width, 1))
        self.health -= bullet.damage / range

    def destroy(self):
        for channel in Global.Clients:
            channel.Send({"action": Global.NetworkActions.DESTROY, "type": "wall", 'id': self.id})

        if self in Global.objects['walls']: Global.objects['walls'].remove(self)

    def getObjectFromSelf(self):
        return {
            'id': self.id,
            'position': self.position,
            'type': self.type
        }