import cocos
from cocos.batch import BatchableNode, BatchNode
from cocos.layer import Layer, director
from cocos.text import Label
import cocos.collision_model as cm
from flask import json

from pyglet.window import key

from ButtonsProvider import ButtonsProvider
from ObjectProvider import ObjectProvider


class MouseInput(Layer):
    is_event_handler = True
    walls = []
    labels = []
    collision = cm.CollisionManagerBruteForce()

    appendMode = 1

    def __init__(self, keyboard):
        super(MouseInput, self).__init__()
        self.keyboard = keyboard
        self.buttonsProvider = ButtonsProvider()
        self.objectProvider = ObjectProvider(self.keyboard, self.collision)

        self.text = Label("mod1",
                          font_name='Helvetica',
                          font_size=16,
                          anchor_x='left',  anchor_y='top'
                          )

        # Then I just add the text!
        #self.add(self.text)

        sublayer = BatchNode()
        for sprite in self.getRightPanel():
            sublayer.add(sprite)
        self.add(sublayer)

    def getRightPanel(self):
        x, y = director.get_window_size()
        sprites = ['l0']

        for sprite in sprites:
            sprite = cocos.sprite.Sprite('walls/' + sprite + '.png')
            sprite.position = x - sprite.width / 2, y + sprite.height / 2

        return sprites

    def addBrick(self, x, y):
        sprite = cocos.sprite.Sprite('walls/l0.png')
        sprite.type = 'brick1'
        sprite.position = x, y
        sprite.scale = 1

        sprite.cshape = cm.AARectShape(
            sprite.position,
            sprite.width // 2,
            sprite.height // 2
        )

        if self.objectProvider.checkIntersec(sprite):
            return

        nearWallPosition = self.objectProvider.getNearObject(x, y, self.walls)
        if nearWallPosition:
            sprite.position = nearWallPosition


        self.walls.append(sprite)
        self.add(sprite)
        self.collision.add(sprite)

    def checkButtons(self, dt):
        if self.keyboard[key.S]:
            self.buttonsProvider.exportToFile(self.walls)


    def removeBrick(self, x, y):
        fakeObj = self.objectProvider.getFakeObject((x,y))
        collisions = self.collision.objs_colliding(fakeObj)
        if collisions:
            for wall in self.walls:
                if wall in collisions:
                    if wall in self.walls: self.walls.remove(wall)
                    if wall in self: self.remove(wall)
                    if wall in self.collision.objs: self.collision.remove_tricky(wall)
                    #if wall in self.collision: self.collision.objs.remove(wall)



    def on_mouse_motion(self, x, y, dx, dy):
        pass
        #self.addBrick(x, y)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        leftClick = buttons == 1
        rightClick = buttons == 4
        if leftClick: self.addBrick(x, y)
        if rightClick: self.removeBrick(x, y)

    def on_mouse_press(self, x, y, buttons, modifiers):
        leftClick = buttons == 1
        rightClick = buttons == 4
        self.position_x, self.position_y = director.get_virtual_coordinates(x, y)
        if leftClick: self.addBrick(x, y)
        if rightClick: self.removeBrick(x, y)