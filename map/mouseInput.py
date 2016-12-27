from copy import copy

import cocos
from cocos.batch import BatchableNode, BatchNode
from cocos.layer import Layer, director, ScrollableLayer
from cocos.text import Label
import cocos.collision_model as cm
from flask import json

from pyglet.window import key

from ButtonsProvider import ButtonsProvider
from ObjectProvider import ObjectProvider
from sprites.destroyableObject import destroyableObject


#class MouseInput(ScrollableLayer):
class MouseInput(Layer):
    is_event_handler = True
    walls = []
    labels = []
    collision = cm.CollisionManagerBruteForce()
    rightPanelCollision = cm.CollisionManagerBruteForce()

    focusX = 1500
    focusY = 500

    currentSprite = None

    appendMode = 1

    def __init__(self, keyboard, scroller):
        super(MouseInput, self).__init__()
        self.keyboard = keyboard
        self.scroller = scroller
        self.buttonsProvider = ButtonsProvider()
        self.objectProvider = ObjectProvider(self.keyboard, self.collision, self.rightPanelCollision)

        self.text = Label("mod1",
                          font_name='Helvetica',
                          font_size=16,
                          anchor_x='left',  anchor_y='top'
                          )

        #self.sublayer = cocos.layer.ScrollableLayer()
        self.sublayer = BatchNode()
        self.rightPanel = []
        self.add(self.sublayer)

        #s = cocos.sprite.Sprite('assets/5x1.jpg')
        #s.position = (100, 100)
        #self.sublayer.add(s)

        map = self.buttonsProvider.getMap()
        if map: self.loadMap(map)

    def resize(self, width, height):
        self.clearRightPanel()
        for sprite in self.getRightPanel(width, height):
            self.sublayer.add(sprite)
            self.rightPanel.append(sprite)

    def clearRightPanel(self):
        for el in self.rightPanel:
            self.sublayer.remove(el)
            self.rightPanelCollision.remove_tricky(el)
        self.rightPanel = []

    def getRightPanel(self, x, y):
        sprites = []
        sp_obj = []
        lastYPos = 0

        for j in range(20):
            for i in range(19):
                sprites.append(str(j)+"x"+str(i)+".jpg")

        count = 0
        columns = 0
        for sprite in sprites:
            src = 'assets/' + sprite
            sprite = cocos.sprite.Sprite(src)
            sprite.src = src

            lastYPos = sprite.height + lastYPos
            lastXPos = x - sprite.width / 2 - 32 * columns
            if count % 19 == 0:
                columns += 1
                lastYPos = 0
            count += 1

            sprite.position = lastXPos, lastYPos
            sprite.cshape = cm.AARectShape(
                sprite.position,
                sprite.width // 2,
                sprite.height // 2
            )
            self.rightPanelCollision.add(sprite)
            sp_obj.append(sprite)

        return sp_obj

    def clickOnRightPanel(self, sprite):
        self.currentSprite = sprite


    def addBrick(self, x, y):
        fakeObj = self.objectProvider.getFakeObject((x,y))
        rightClickedBlock = self.objectProvider.checkIntersecWithRightPanel(fakeObj)
        if rightClickedBlock:
            return self.clickOnRightPanel(rightClickedBlock)

        if not self.currentSprite: return

        sprite = cocos.sprite.Sprite(self.currentSprite.src)
        sprite.type = 'background'
        sprite.src = self.currentSprite.src
        sprite.position = x // 32 * 32, y // 32 * 32
        #sprite.position = x, y

        sprite.cshape = cm.AARectShape(
            sprite.position,
            sprite.width // 2,
            sprite.height // 2
        )

        if self.objectProvider.checkIntersec(sprite):
            return

        # nearWallPosition = self.objectProvider.getNearObject(x, y, self.walls)
        # if nearWallPosition:
        #     sprite.position = nearWallPosition


        self.walls.append(sprite)
        self.add(sprite)
        self.collision.add(sprite)

    def checkButtons(self, dt):
        x_direction = self.keyboard[key.RIGHT] - self.keyboard[key.LEFT]
        y_direction = self.keyboard[key.UP] - self.keyboard[key.DOWN]

        if x_direction:
            self.focusX += x_direction * 20

        if y_direction:
            self.focusY += y_direction * 20

        if x_direction or y_direction:
            pass#self.scroller.set_focus(self.focusX, self.focusY)

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


    def loadMap(self, map):
        for block in map:
            sprite = destroyableObject(block)
            self.addSpriteToObjects(sprite)

    def addSpriteToObjects(self, sprite):
        self.walls.append(sprite)
        self.add(sprite)
        self.collision.add(sprite)

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
        print(self.position_x)
        if leftClick: self.addBrick(x, y)
        if rightClick: self.removeBrick(x, y)