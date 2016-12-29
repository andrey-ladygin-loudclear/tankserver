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
    def checkWithObjects(object, parent_id = None):
        for player in Global.objects['players']:

            if parent_id == player.id: continue

            player_points = player.getPoints()
            if Collisions.check(player_points, object.position):
                return True

        for enemy in Global.objects['enemies']:

            if parent_id == enemy.id: continue

            enemy_points = enemy.getPoints()
            if Collisions.check(enemy_points, object.position):
                return True

        return False

    @staticmethod
    def checkManualCollisionsWidthWalls(object):
        object_points = object.getPoints()

        for wall in Global.objects['walls']:
            wall_points = wall.getPoints()

            if Collisions.intersection(object_points, wall_points):
                return True

    @staticmethod
    def intersection(object1, object2):
        # o1_x1, o1_x2, o1_x3, o1_x4 = object1
        # o2_x1, o2_x2, o2_x3, o2_x4 = object2

        # Global.Queue.append({
        #     'action': Global.NetworkActions.TEST,
        #     Global.NetworkDataCodes.POSITION: ((o1_x1, o1_x2), (o1_x2, o1_x3), (o1_x3, o1_x4), (o1_x4, o1_x1))
        # })

        for corner_tank_point in object1:
            if Collisions.check(object2, corner_tank_point):
                return True

        return False

    @staticmethod
    def check(points, check_point):
        sum = 0
        px = check_point[0]
        py = check_point[1]

        for k in range(len(points)):
            x1 = points[k][0] - px
            y1 = points[k][1] - py

            try:
                x2 = points[k + 1][0] - px
                y2 = points[k + 1][1] - py
            except IndexError:
                x2 = points[0][0] - px
                y2 = points[0][1] - py

            s1 = (x1*x1 + y1*y1 - x2*x1 - y2*y1)
            d1 = (x1*y2 - x2*y1) + 0.0000001
            s2 = (x2*x2 + y2*y2 - x2*x1 - y2*y1)
            d2 = (x1*y2 - x2*y1) + 0.0000001
            sum += math.atan(s1 / d1) + math.atan(s2 / d2)

        return math.fabs(sum) > 0.01
