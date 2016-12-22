import cocos
from cocos.batch import BatchableNode
from cocos.layer import Layer, director
from cocos.text import Label
import cocos.collision_model as cm


class MouseInput(Layer):
    is_event_handler = True
    walls = []
    collision = cm.CollisionManagerBruteForce()

    def __init__(self):
        super(MouseInput, self).__init__()

        # This time I set variables for the position rather than hardcoding it
        # I do this because we will want to alter these values later
        self.position_x = 100
        self.position_y = 240

        # Once again I make a label
        self.text = Label("No mouse interaction yet",
                          font_name = "Helvetica",
                          font_size = 24,
                          x = self.position_x,
                          y = self.position_y)

        # Then I just add the text!
        #self.add(self.text)

    # Like last time we need to make a function to update that self.text label to display the mouse data
    def addBrick(self, x, y):
        sprite = cocos.sprite.Sprite('walls/brick1.png')
        sprite.position = x, y
        sprite.scale = 1

        sprite.cshape = cm.AARectShape(
            sprite.position,
            sprite.width // 2,
            sprite.height // 2
        )

        if self.checkIntersec(sprite):
            return

        self.walls.append(sprite)
        self.add(sprite)
        self.collision.add(sprite)

    def removeBrick(self, x, y):
        fakeObj = self.getFakeObject((x,y))
        collisions = self.collision.objs_colliding(fakeObj)
        if collisions:
            for wall in self.walls:
                if wall in collisions:
                    if wall in self.walls: self.walls.remove(wall)
                    if wall in self: self.remove(wall)
                    if wall in self.collision.objs: self.collision.remove_tricky(wall)
                    #if wall in self.collision: self.collision.objs.remove(wall)

    def checkIntersec(self, object):
        collisions = self.collision.objs_colliding(object)

        if collisions:
            return True

        return False

    def getFakeObject(self, position, width = 2, height = 2):
        obj = BatchableNode()
        obj.cshape = cm.AARectShape(position,width // 2,height // 2)
        return obj

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