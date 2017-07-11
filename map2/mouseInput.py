from time import sleep

import cocos
from cocos import sprite
from cocos.batch import BatchableNode, BatchNode
from cocos.layer import Layer, director, ScrollableLayer
from cocos.text import Label
import cocos.collision_model as cm
from flask import json

from pyglet.window import key
from scandir import scandir

from ButtonsProvider import ButtonsProvider
from ObjectProvider import ObjectProvider
from SpriteFactory import SpriteFactory


class MouseInput(ScrollableLayer):
#class MouseInput(Layer):
    is_event_handler = True
    walls = []
    labels = []
    collision = cm.CollisionManagerBruteForce()
    palitraCollision = cm.CollisionManagerBruteForce()

    focusX = 1500
    focusY = 500

    currentType = 'background'
    currentSprite = None

    appendMode = 1

    def __init__(self, keyboard, scroller):
        super(MouseInput, self).__init__()
        self.keyboard = keyboard
        self.scroller = scroller
        #self.buttonsProvider = ButtonsProvider()
        self.objectProvider = ObjectProvider(self.keyboard, self.collision, self.palitraCollision)

        self.text = Label("Some text", font_name='Helvetica', font_size=12, anchor_x='left',  anchor_y='bottom')
        self.text.position = (0,0)
        self.add(self.text, z=5)

        #self.sublayer = cocos.layer.ScrollableLayer()

        self.palitra = cocos.layer.Layer()
        self.palitraObject = []
        self.add(self.palitra, z=2)
        self.loadMap()


        # for sprite in self.getRightPanel():
        #     self.palitra.add(sprite)
        #     self.rightPanel.append(sprite)

        # map = self.buttonsProvider.getMap()
        # if map: self.loadMap(map)

    def loadMap(self):
        for file in scandir('assets'):
            src = 'assets/' + str(file.name)
            land = sprite.Sprite(src)
            land.cshape = cm.AARectShape(land.position,land.width//2,land.height//2)
            land.src = src
            self.palitra.add(land)
            self.palitraObject.append(land)
            self.palitraCollision.add(land)


    def resizeMap(self):
        col = 0
        row = 0
        for land in self.palitraObject:
            x = land.width * .5 + land.width * col + 2 - self.currentWidth // 2
            y = land.height * .5 + land.height * row + 2 - self.currentHeight // 2
            col += 1
            if col > 20:
                row += 1
                col = 0
            land.position = (x, y)
            land.cshape = cm.AARectShape(land.position,land.width//2,land.height//2)


    def checkButtons(self, dt):
        x_direction = self.keyboard[key.RIGHT] - self.keyboard[key.LEFT]
        y_direction = self.keyboard[key.UP] - self.keyboard[key.DOWN]

        if self.keyboard[key.Q]:
            self.palitra.visible = 1 - self.palitra.visible
            sleep(0.1)

        # if x_direction:
        #     self.focusX += x_direction * 50
        #
        # if y_direction:
        #     self.focusY += y_direction * 50
        #
        # if x_direction or y_direction:
        #     w, h = cocos.director.director.get_window_size()
        #     self.resize(w + self.focusX - 2032, h + self.focusY - 20*32)
        #     self.scroller.set_focus(self.focusX, self.focusY)
        #
        # if self.keyboard[key.T]:
        #     self.buttonsProvider.toggleDestoyableObjects(self.walls, self, self.collision)
        #
        # if self.keyboard[key.S]:
        #     self.buttonsProvider.exportToFile(self.walls)

    def resize(self, width, height):
        self.text.position = (-width//2, -height//2)
        self.currentWidth = width
        self.currentHeight = height

        self.resizeMap()

    def on_mouse_motion(self, x, y, dx, dy):
        pass
        #self.addBrick(x, y)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        print 'mouse drag'

    def on_mouse_press(self, x, y, buttons, modifiers):
        #print 'mouse click'

        leftClick = buttons == 1
        rightClick = buttons == 4

        x = x - self.currentWidth//2
        y = y - self.currentHeight//2

        if self.palitra.visible:
            if leftClick: self.selectBrick(x, y)
        else:
            if leftClick and self.currentSprite: self.addBrick(x, y)
            if rightClick: self.removeBrick(x, y)

        sleep(0.01)

        info = "press: " + str(x) + ',' + str(y)
        info += ", width: " + str(self.currentWidth) + ", height: " + str(self.currentHeight)
        if self.currentSprite: info += ", currentSprite: " + str(self.currentSprite.image)

        self.text.element.text = info

    def selectBrick(self, x, y):
        fakeObj = self.objectProvider.getFakeObject((x,y))
        selectedSprite = self.objectProvider.checkIntersecWithRightPanel(fakeObj)
        if selectedSprite:
            self.currentSprite = selectedSprite
        else:
            self.currentSprite = None

    def addBrick(self, x, y):
        spriteObj = sprite.Sprite(self.currentSprite.src)
        spriteObj.position = (x, y)
        spriteObj.cshape = cm.AARectShape(spriteObj.position,spriteObj.width//2,spriteObj.height//2)

        intersec = self.objectProvider.checkIntersec(spriteObj)
        if intersec: return

        self.collision.add(spriteObj)
        self.add(spriteObj)

    def removeBrick(self, x, y):
        pass