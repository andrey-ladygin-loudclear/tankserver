from cocos import sprite
import cocos.collision_model as cm


class destroyableObject(sprite.Sprite):
    def __init__(self, object):
        self.type = object.get('type')

        #self.src = 'walls/l0.png'

        #if self.type == 'brick':
        self.src = str(object.get('src'))

        super(destroyableObject, self).__init__(self.src)

        self.position = object.get('position')

        self.cshape = cm.AARectShape(
            self.position,
            self.width // 2,
            self.height // 2
        )