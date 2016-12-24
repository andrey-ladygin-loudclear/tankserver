import cocos
from pyglet.window import key
from mouseInput import MouseInput

global keyboard

cocos.director.director.init(do_not_scale=True, resizable=True)


keyboard = key.KeyStateHandler()
cocos.director.director.window.push_handlers(keyboard)

mouseInputHandler = MouseInput(keyboard)

scene = cocos.scene.Scene(mouseInputHandler)
scene.schedule(mouseInputHandler.checkButtons)

cocos.director.director.run(scene)
