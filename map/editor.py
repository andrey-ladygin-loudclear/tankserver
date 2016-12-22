import cocos

from mouseInput import MouseInput

cocos.director.director.init()

scene = cocos.scene.Scene(MouseInput())

cocos.director.director.run(scene)