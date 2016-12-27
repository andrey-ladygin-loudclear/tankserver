import cocos
import pyglet
from pyglet.window import key
from mouseInput import MouseInput

global keyboard, scroller

cocos.director.director.init(autoscale=False, resizable=True, width=3000, height=1000)

keyboard = key.KeyStateHandler()
scroller = cocos.layer.ScrollingManager()
cocos.director.director.window.push_handlers(keyboard)
#cocos.director.director.window.push_handlers(scroller)

mouseInputHandler = MouseInput(keyboard, scroller)
scroller.add(mouseInputHandler)

scene = cocos.scene.Scene(mouseInputHandler, scroller)
scene.schedule(mouseInputHandler.checkButtons)

cocos.director.director.on_resize = mouseInputHandler.resize

cocos.director.director.run(scene)