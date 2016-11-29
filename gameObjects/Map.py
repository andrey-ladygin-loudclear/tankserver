import Global
from gameObjects.Wall import Wall
import cocos.collision_model as cm


class Map:
    def get_walls(self):
        if len(Global.objects['walls']):
            return Global.objects['walls']

        for i in range(20):
            wall = Wall()
            wall.id = Global.game.getNextId()
            wall.type = 'BrickWall'
            wall.position = (i*32, 300)

            wall.cshape = cm.AARectShape(
                wall.position,
                wall.width // 2 - 2,
                wall.height // 2 - 2
            )
            Global.objects['walls'].append(wall)
            Global.collision_manager.add(wall)

        for i in range(20):
            wall = Wall()
            wall.id = Global.game.getNextId()
            wall.type = 'BrickWall'
            wall.position = (i*32, 500)

            wall.cshape = cm.AARectShape(
                wall.position,
                wall.width // 2 - 2,
                wall.height // 2 - 2
            )
            Global.objects['walls'].append(wall)
            Global.collision_manager.add(wall)

        for i in range(30):
            wall = Wall()
            wall.id = Global.game.getNextId()
            wall.type = 'BrickWall'
            wall.position = (i*32 + 680, 500)

            wall.cshape = cm.AARectShape(
                wall.position,
                wall.width // 2 - 2,
                wall.height // 2 - 2
            )
            Global.objects['walls'].append(wall)
            Global.collision_manager.add(wall)

        return Global.objects['walls']