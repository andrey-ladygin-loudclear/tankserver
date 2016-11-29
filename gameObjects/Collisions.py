import math

import Global


class Collisions:

    @staticmethod
    def checkWithWalls(object):
        collisions = Global.collision_manager.objs_colliding(object)

        if collisions:
            for wall in Global.objects['walls']:
                if wall in collisions:
                    return True

        return False

    @staticmethod
    def checkManualCollisionsWidthWalls(object):
        w, h = object.width, object.height
        scale = object.scale
        x, y = object.position
        cos_x = math.cos(math.radians(object.rotation + 180))
        sin_x = math.sin(math.radians(object.rotation + 180))
        x1, y1 = (x - w//2 * scale) * sin_x, (y - h//2 * scale) * cos_x
        x2, y2 = (x + w//2 * scale) * sin_x, (y - h//2 * scale) * cos_x
        x3, y3 = (x + w//2 * scale) * sin_x, (y + h//2 * scale) * cos_x
        x4, y4 = (x - w//2 * scale) * sin_x, (y + h//2 * scale) * cos_x

        # Global.Queue.append({'action': Global.NetworkActions.TEST, Global.NetworkDataCodes.TYPE: 'clear'})
        # Global.Queue.append({'action': Global.NetworkActions.TEST, Global.NetworkDataCodes.POSITION: (x1, y1)})
        # Global.Queue.append({'action': Global.NetworkActions.TEST, Global.NetworkDataCodes.POSITION: (x2, y2)})
        # Global.Queue.append({'action': Global.NetworkActions.TEST, Global.NetworkDataCodes.POSITION: (x3, y3)})
        # Global.Queue.append({'action': Global.NetworkActions.TEST, Global.NetworkDataCodes.POSITION: (x4, y4)})

        for wall in Global.objects['walls']:
            if self.intersection(wall, )

