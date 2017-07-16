import Global
import cocos.collision_model as cm


class ObjectsManager:
    objects = []

    def add(self, object):
        self.objects.append(object)
        object.cshape = cm.AARectShape(object.position, object.width//2, object.height//2)
        Global.collision_manager.add(object)