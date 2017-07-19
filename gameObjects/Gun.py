
class Gun():

    weapon1 = None
    weapon2 = None

    canFire = True
    canHeavyFire = True

    tank = None

    def __init__(self, spriteName, tank):
        self.weapon1 = HeavyWeapon(self)
        self.weapon2 = LightWeapon(self)
        self.tank = tank

    def fireFirstWeapon(self):
        self.weapon1.fire()

    def fireSecondWeapon(self):
        self.weapon2.fire()

    def getRotation(self):
        return self.rotation