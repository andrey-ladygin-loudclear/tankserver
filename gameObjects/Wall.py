import cocos.collision_model as cm

class Wall():
    id = 0

    def update_position(self, position):
        self.position = position
        self.cshape = cm.AARectShape(
            self.position,
            32 // 2,
            32 // 2
        )