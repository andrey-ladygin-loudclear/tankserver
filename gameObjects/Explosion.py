import cocos.collision_model as cm
import cocos.euclid as eu

import Global
from gameObjects.Collisions import Collisions


class Explosion():
    def __init__(self, bullet):
        center_x, center_y = bullet.position
        self.radius = bullet.damageRadius
        self.cshape = cm.CircleShape(eu.Vector2(center_x, center_y), bullet.damageRadius)
        self.bullet = bullet

    def checkDamageCollisions(self):
        damage_collisions = Global.collision_manager.objs_colliding(self)

        if damage_collisions:
            for damage_wall in Global.objects['walls']:
                if damage_wall in damage_collisions:
                    damage_wall.damage(self.bullet)


        for player in Global.objects['players']:

            #if parent_id == player.id: continue

            player_points = player.getPoints()
            if Collisions.check(player_points, self.bullet.position):
                player.damage(self.bullet)

        for enemy in Global.objects['enemies']:

            #f parent_id == enemy.id: continue

            enemy_points = enemy.getPoints()
            if Collisions.check(enemy_points, self.bullet.position):
                enemy_points.damage(self.bullet)