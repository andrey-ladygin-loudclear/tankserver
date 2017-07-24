import json

import cocos.collision_model as cm

from Landing.Center import Center
from Landing.LandingObject import LandingObject
from helper import Global


class Map:
    walls = []

    def get_map(self):
        with open('map2/exportMap.json', 'r') as f:
            read_data = f.read()

        return json.loads(read_data)

    def init_walls(self):

        map = self.get_map()

        for object in map:

            #1 - background, 2 - unmovable background, 3 - indestructible object, 4 - object

            wall = LandingObject()
            wall.type = object.get('type')
            wall.id = Global.game.getNextId()
            wall.src = object.get('src')
            wall.set_position(object.get('position'))

            self.walls.append(wall)

            if wall.type != 0 and wall.type != 1:
                Global.GameObjects.addWall(wall)
                # Global.objects['walls'].append(wall)
                # Global.collision_manager.add(wall)

        self.addCenters()

    def get_walls(self):
        return self.walls

    def addCenters(self):
        center1 = self.addCenter((1140, 350), 1)
        center2 = self.addCenter((1140, 3870 - 350), 2)

        Global.GameObjects.setCenter(center1, 1)
        Global.GameObjects.setCenter(center2, 2)

    def addCenter(self, position, clan):
        center = Center()
        center.id = Global.game.getNextId()
        center.src = 'assets/buildings/center.png'
        center.set_position(position)
        center.clan = clan
        Global.GameObjects.addWall(center)
        self.walls.append(center)
        return center