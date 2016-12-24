class ObjectProvider:
    def checkIntersec(self, object):
        collisions = self.collision.objs_colliding(object)

        if collisions:
            return True

        return False

    def getFakeObject(self, position, width = 2, height = 2):
        obj = BatchableNode()
        obj.cshape = cm.AARectShape(position,width // 2,height // 2)
        return obj

    def getNearObject(self, x, y):
        dx = 20
        wall = self.getObjectByPoints(x - dx, y)
        if wall:
            x, y = wall.position
            return (x + wall.width, y)

        wall = self.getObjectByPoints(x + dx, y)
        if wall:
            x, y = wall.position
            return (x - wall.width, y)

        wall = self.getObjectByPoints(x, y + dx)
        if wall:
            x, y = wall.position
            return (x, y - wall.height)

        wall = self.getObjectByPoints(x, y - dx)
        if wall:
            x, y = wall.position
            return (x, y + wall.height)

    def getObjectByPoints(self, x, y):
        fakeObj = self.getFakeObject((x,y))
        collisions = self.collision.objs_colliding(fakeObj)
        if collisions:
            for wall in self.walls:
                if wall in collisions: return wall