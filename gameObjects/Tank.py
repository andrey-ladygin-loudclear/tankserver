import Global

from gameObjects.bullets.StandartBullet import StandartBullet


class Tank:
    id = 0
    tankClass = ''
    fraction = ''
    rotation = 0
    position = (0, 0)

    def getObjectFromSelf(self):
        return {
            'id': self.id,
            'position': self.position,
            'rotation': self.rotation,
            'fraction': self.fraction,
            'tankClass': self.tankClass,
            'type': 'tank',
        }

    def fire(self, bulletObj):
        bullet = StandartBullet()
        bullet.position = bulletObj.get('pos')
        bullet.rotation = bulletObj.get('rotation')

        Global.objects['bullets'].append(bullet)