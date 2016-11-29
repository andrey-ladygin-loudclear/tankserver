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

        object_points = Collisions.getPointsFromDimensions(w, h, x, y, rotation, scale)

        # Global.Queue.append({'action': Global.NetworkActions.TEST, Global.NetworkDataCodes.TYPE: 'clear'})
        # Global.Queue.append({'action': Global.NetworkActions.TEST, Global.NetworkDataCodes.POSITION: (x1, y1)})
        # Global.Queue.append({'action': Global.NetworkActions.TEST, Global.NetworkDataCodes.POSITION: (x2, y2)})
        # Global.Queue.append({'action': Global.NetworkActions.TEST, Global.NetworkDataCodes.POSITION: (x3, y3)})
        # Global.Queue.append({'action': Global.NetworkActions.TEST, Global.NetworkDataCodes.POSITION: (x4, y4)})

        for wall in Global.objects['walls']:
            w, h = wall.width, wall.height
            scale = wall.scale
            x, y = wall.position
            wall_points = Collisions.getPointsFromDimensions(w, h, x, y, 0, scale)
            if Collisions.intersection(object_points, wall_points):
                print('COLLISION WITH TANK')

    @staticmethod
    def intersection(object1, object2):
        p11, p12, p13, p14 = object1
        p21, p22, p23, p24 = object2

        return Collisions.inPolygon()

        #double x1,y1,x2,y2,x,y;
        #// (x1,y1) - координаты левой верхней точки прямоугольника
        #// (x2,y2) - координаты правой нижней точки прямоугольника
        #// (x,y) - координаты проверяемой точки

        #if x>=x1 && y>=y1 && x<=x2 && y<=y2:
        #    return True

# var intersects = function ( a, b ) {
# return ( a.y < b.y1 || a.y1 > b.y || a.x1 < b.x || a.x > b.x1 );
# }

    @staticmethod
    def intersect(A,B,C,D):
        return Collisions.rotate(A,B,C)*Collisions.rotate(A,B,D)<=0 and Collisions.rotate(C,D,A)*Collisions.rotate(C,D,B)<0

    @staticmethod
    def rotate(A,B,C):
        return (B[0]-A[0])*(C[1]-B[1])-(B[1]-A[1])*(C[0]-B[0])

    def inPolygon(x, y, xp, yp):
        c=0
        for i in range(len(xp)):
            if (((yp[i]<=y and y<yp[i-1]) or (yp[i-1]<=y and y<yp[i])) and (x > (xp[i-1] - xp[i]) * (y - yp[i]) / (yp[i-1] - yp[i]) + xp[i])): c = 1 - c
        return c
        #print( inPolygon(100, 0, (-100, 100, 100, -100), (100, 100, -100, -100)))

    @staticmethod
    def getPointsFromDimensions(w, h, x, y, rotation = 0, scale = 1):
        cos_x = math.cos(math.radians(rotation + 180))
        sin_x = math.sin(math.radians(rotation + 180))
        x1, y1 = (x - w//2 * scale) * sin_x, (y - h//2 * scale) * cos_x
        x2, y2 = (x + w//2 * scale) * sin_x, (y - h//2 * scale) * cos_x
        x3, y3 = (x + w//2 * scale) * sin_x, (y + h//2 * scale) * cos_x
        x4, y4 = (x - w//2 * scale) * sin_x, (y + h//2 * scale) * cos_x

        return ((x1, y1),(x2, y2),(x3, y3),(x4, y4))
