from helper import Global


class Objects:
    game = None
    globalPanel = None
    walls = []
    backgrounds = []
    bullets = []
    tanks = []
    centers = {}

    def addTank(self, tank):
        self.tanks.append(tank)
        Global.CollisionManager.add(tank)

    def getTanks(self):
        return self.tanks

    def getTank(self, id):
        for tank in self.tanks:
            if tank.id == id: return tank

        return None

    def removeTank(self, tank):
        self.tanks.remove(tank)
        Global.CollisionManager.remove_tricky(tank)

    def addWall(self, wall):
        self.walls.append(wall)
        Global.CollisionManager.add(wall)

    def getWalls(self):
        return self.walls

    def removeWall(self, wall):
        self.walls.remove(wall)

    def removeAnimation(self, anim):
        self.globalPanel.remove(anim)

    def addBullet(self, bullet):
        self.bullets.append(bullet)

    def getBullets(self):
        return self.bullets

    def removeBullet(self, bullet):
        self.bullets.remove(bullet)

    def setCenter(self, center, clan):
        self.centers[clan] = center

    def getCenter(self, clan):
        return self.centers[clan]
