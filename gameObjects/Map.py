import json

import Global
import cocos.collision_model as cm

from gameObjects.landing.decorationObject import decorationObject
from gameObjects.landing.destroyableObject import destroyableObject


class Map:
    def get_map(self):
        with open('map/exportMap.json', 'r') as f:
            read_data = f.read()

        return json.loads(read_data)

    def get_walls(self):
        if len(Global.objects['walls']):
            return Global.objects['walls']

        map = self.get_map()

        for object in map:
            if object.get('type') == 'decoration':
                wall = decorationObject()
            if object.get('type') == 'destroyable':
                wall = destroyableObject()

            wall.id = Global.game.getNextId()
            wall.set_position(object.get('position'))
            Global.objects['walls'].append(wall)
            Global.collision_manager.add(wall)

        return Global.objects['walls']