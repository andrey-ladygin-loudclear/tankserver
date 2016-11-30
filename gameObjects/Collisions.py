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
        rotation = object.rotation

        object_points = object.getPoints()

        # Global.Queue.append({'action': Global.NetworkActions.TEST, Global.NetworkDataCodes.TYPE: 'clear'})
        # Global.Queue.append({'action': Global.NetworkActions.TEST, Global.NetworkDataCodes.POSITION: (x1, y1)})
        # Global.Queue.append({'action': Global.NetworkActions.TEST, Global.NetworkDataCodes.POSITION: (x2, y2)})
        # Global.Queue.append({'action': Global.NetworkActions.TEST, Global.NetworkDataCodes.POSITION: (x3, y3)})
        # Global.Queue.append({'action': Global.NetworkActions.TEST, Global.NetworkDataCodes.POSITION: (x4, y4)})

        for wall in Global.objects['walls']:
            wall_points = wall.getPoints()

            if wall.position == (32, 300):
                if Collisions.intersection(object_points, wall_points):
                    print('COLLISION WITH TANK')

    @staticmethod
    def intersection(object1, object2):
        o1_x1, o1_y1, o1_x2, o1_y2 = object1
        o2_x1, o2_y1, o2_x2, o2_y2 = object2

        #print('TANK')
        print(o1_x1, o1_y1, o1_x2, o1_y2)
        #print('WALL')
        #print(o2_x1, o2_y1, o2_x2, o2_y2)
        #print('')

        if o1_x1 > o2_x1 and o1_y1 > o2_y1 and o1_x2 < o2_x2 and o1_y2 < o2_y2:
            return True


        return False
        #double x1,y1,x2,y2,x,y;

        #if x>=x1 && y>=y1 && x<=x2 && y<=y2:
        #    return True

    #@staticmethod
    #def intersect(A,B):
        #return A[1] < B[3] or A[3] > b.y || a.x1 < b.x || a.x > b.x1

    @staticmethod
    def getPointsFromDimensions(w, h, x, y, rotation = 0, scale = 1):
        cos_x = math.cos(math.radians(rotation + 180))
        sin_x = math.sin(math.radians(rotation + 180))
        x1, y1 = (x - w//2 * scale) * sin_x, (y - h//2 * scale) * cos_x
        x2, y2 = (x + w//2 * scale) * sin_x, (y - h//2 * scale) * cos_x
        x3, y3 = (x + w//2 * scale) * sin_x, (y + h//2 * scale) * cos_x
        x4, y4 = (x - w//2 * scale) * sin_x, (y + h//2 * scale) * cos_x

        min_x = min(x1, x2, x3, x4)
        min_y = min(y1, y2, y3, y4)
        max_x = max(x1, x2, x3, x4)
        max_y = max(y1, y2, y3, y4)
        return (min_x, min_y,max_x, max_y)
