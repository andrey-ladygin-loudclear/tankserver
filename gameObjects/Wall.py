import math

import Global


class Wall():
    id = 0
    health = 20
    position = (0, 0)

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
            Global.NetworkDataCodes.TYPE: Global.NetworkDataCodes.WALL,
            Global.NetworkDataCodes.POSITION: self.position,
            Global.NetworkDataCodes.ID: self.id
        })

        if self in Global.objects['walls']: Global.objects['walls'].remove(self)


    def getPoints(self):
        x, y = self.position
        w, h = (self.width * self.scale, self.height * self.scale)
        x1, y1 = x, y
        x2, y2 = x + w, y
        x3, y3 = x + w, y + h
        x4, y4 = x, y + h

        return ((x1, y1),(x2, y2),(x3, y3),(x4, y4))

    def getObjectFromSelf(self):
        return {
            'action': Global.NetworkActions.UPDATE,
            Global.NetworkDataCodes.ID: self.id,
            Global.NetworkDataCodes.POSITION: self.position,
            Global.NetworkDataCodes.TYPE: Global.NetworkDataCodes.WALL
        }