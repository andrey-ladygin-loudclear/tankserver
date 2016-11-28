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