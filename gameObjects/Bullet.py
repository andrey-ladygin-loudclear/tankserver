class Bullet:
    def explosion(self):
        animation = self.getExplosionAnimation()
        anim = self.getExplosionAnimationSprite(animation)

        Global.layers['game'].add(anim)

        self.removeAnimation()

        t = Timer(animation.get_duration(), lambda: Global.layers['game'].remove(anim))
        t.start()

        return Explosion(self)