import cocos.collision_model as cm
import cocos.euclid as eu

from gameObjects.Collisions import Collisions
from helper import Global


class Explosion():
    def __init__(self, bullet):
        center_x, center_y = bullet.position
        self.radius = bullet.damageRadius
        self.cshape = cm.CircleShape(eu.Vector2(center_x, center_y), bullet.damageRadius)
        self.bullet = bullet

    def checkDamageCollisions(self):
        for player in Global.GameObjects.getTanks():
            player.cshape = cm.AARectShape(
                player.position,
                player.width // 2,
                player.height // 2
            )

        # for enemy in Global.objects['enemies']:
        #     enemy.cshape = cm.AARectShape(
        #         enemy.position,
        #         enemy.width // 2,
        #         enemy.height // 2
        #     )

        damage_collisions = Global.CollisionManager.objs_colliding(self)

        if damage_collisions:
            for damage_wall in Global.GameObjects.getWalls():
                if damage_wall.type == 'destroyable':
                    if damage_wall in damage_collisions:
                        damage_wall.damage(self.bullet)

            for player in Global.GameObjects.getTanks():
                if player in damage_collisions:
                    player.damage(self.bullet)

            # for enemy in Global.objects['enemies']:
            #     if enemy in damage_collisions:
            #         enemy.damage(self.bullet)


    def checkDamageCollisionsOLD(self):
        damage_collisions = Global.CollisionManager.objs_colliding(self)

        if damage_collisions:
            for damage_wall in Global.GameObjects.getWalls():
                if damage_wall in damage_collisions:
                    damage_wall.damage(self.bullet)


        for player in Global.GameObjects.getTanks():

            #if parent_id == player.id: continue

            player_points = player.getPoints()
            if Collisions.check(player_points, self.bullet.position):
                player.damage(self.bullet)

        # for enemy in Global.objects['enemies']:
        #
        #     #f parent_id == enemy.id: continue
        #
        #     enemy_points = enemy.getPoints()
        #     if Collisions.check(enemy_points, self.bullet.position):
        #         enemy_points.damage(self.bullet)