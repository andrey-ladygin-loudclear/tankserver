import json

import Global
import cocos.collision_model as cm

from gameObjects.landing.backgroundObject import backgroundObject
from gameObjects.landing.decorationObject import decorationObject
from gameObjects.landing.destroyableObject import destroyableObject


class Map:
    walls = []

    def get_map(self):
        with open('map/exportMap.json', 'r') as f:
            read_data = f.read()

        return json.loads(read_data)

    def get_walls(self):
        if len(self.walls):
            return self.walls

        map = self.get_map()

        for object in map:

            if object.get('type') == 'decoration':
                wall = decorationObject()

            if object.get('type') == 'destroyable':
                wall = destroyableObject()

            if object.get('type') == 'background':
                wall = backgroundObject()

            wall.id = Global.game.getNextId()
            wall.src = object.get('src')
            wall.set_position(object.get('position'))

            self.walls.append(wall)

            if object.get('type') != 'background':
                Global.objects['walls'].append(wall)
                Global.collision_manager.add(wall)

        return self.walls