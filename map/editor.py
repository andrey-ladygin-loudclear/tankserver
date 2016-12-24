import cocos
from pyglet.window import key
from mouseInput import MouseInput

global keyboard

class test(cocos.director.director):
    def __init__(self, *args, **kwargs):
        self.init(*args, **kwargs)

    def scaled_resize_window(self, width, height):
        super(test, self).scaled_resize_window(width, height)
        print(width)

#cocos.director.director.init(autoscale=False, resizable=True, )
c = test(do_not_scale=True, resizable=True)

keyboard = key.KeyStateHandler()
cocos.director.director.window.push_handlers(keyboard)

mouseInputHandler = MouseInput(keyboard)

scene = cocos.scene.Scene(mouseInputHandler)
scene.schedule(mouseInputHandler.checkButtons)

cocos.director.director.run(scene)
