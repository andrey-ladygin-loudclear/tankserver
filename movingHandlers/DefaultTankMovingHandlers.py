import math

import operator
from cocos import actions
import cocos.collision_model as cm

import Global


class DefaultTankMovingHandlers(actions.Move):

    speed = 0

    RIGHT = None
    LEFT = None
    UP = None
    DOWN = None
    GUN_LEFT = None
    GUN_RIGHT = None
    FIRE_HEAVY_GUN = None
    FIRE_LIGHT_GUN = None

    # step() is called every frame.
    # dt is the number of seconds elapsed since the last call.
    def step(self, dt):
        super(DefaultTankMovingHandlers, self).step(dt) # Run step function on the parent class.

        turns_direction = Global.CurrentKeyboard[self.RIGHT] - Global.CurrentKeyboard[self.LEFT]
        moving_directions = Global.CurrentKeyboard[self.UP] - Global.CurrentKeyboard[self.DOWN]
        gun_turns_direction = Global.CurrentKeyboard[self.GUN_RIGHT] - Global.CurrentKeyboard[self.GUN_LEFT]

        # if turns_direction or moving_directions or gun_turns_direction:
        #     Global.TankNetworkListenerConnection.Send({
        #         'action': Global.NetworkActions.TANK_MOVE,
        #         'pos': self.target.position,
        #         'turn': turns_direction,
        #         'mov': moving_directions,
        #         'gun_turn': gun_turns_direction,
        #         'id': self.target.id
        #     })

        if Global.CurrentKeyboard[self.FIRE_LIGHT_GUN]:
            self.target.fire()

        if Global.CurrentKeyboard[self.FIRE_HEAVY_GUN]:
            self.target.heavy_fire()

        self.addSpeed(moving_directions)

        # Set the object's velocity.
        self.setTankRotation(turns_direction, moving_directions)
        new_velocity = self.getVelocity()

        new_position = tuple(map(operator.add, self.target.position, new_velocity))

        if self.checkCollisionsWithObjects():
            self.target.velocity = (0, 0)
            self.target.position = self.target.old_position
        else:
            self.target.old_position = self.target.position

            # if(self.target.position != new_position):
                # Global.TankNetworkListenerConnection.Send({
                #     'action': Global.NetworkActions.TANK_MOVE,
                #     'pos': self.target.position,
                #     'id': self.target.id
                # })
                # Global.TankNetworkListenerConnection.Send({
                #     'action': Global.NetworkActions.TANK_MOVE,
                #     'pos': self.target.position,
                #     'turn': turns_direction,
                #     'mov': moving_directions,
                #     'gun_turn': gun_turns_direction,
                #     'id': self.target.id
                # })

            new_velocity = self.getVelocityByNewPosition(self.target.position, new_position)
            self.setNewVelocity(new_velocity)


        # SHOULD REDUCE SPEED IF NEXT POSITION IS WALL
        #self.setNewVelocity(new_velocity)
        self.setGunPosition()

        # Set the object's rotation
        self.setGunRotation(gun_turns_direction)

    def checkCollisionsWithObjects(self):
        self.target.cshape = cm.AARectShape(
            self.target.position,
            self.target.width // 2,
            self.target.height // 2
        )
        collisions = Global.CollisionManager.objs_colliding(self.target)

        if collisions:
            return True

        return False

    def getVelocityByNewPosition(self, current_position, new_position):
        curr_x, curr_y = current_position
        new_x, new_y = new_position
        diff_x = new_x - curr_x
        diff_y = new_y - curr_y

        return (diff_x, diff_y)


    def setTankRotation(self, turns_direction, moving_directions):
        self.target.rotation = self.getTankRotation(turns_direction, moving_directions)

    def setNewVelocity(self, velocity):
        self.target.velocity = velocity

    def getTankRotation(self, turns_direction, moving_directions):
        tank_rotate = self.target.rotation_speed * turns_direction

        if moving_directions:
            tank_rotate *= moving_directions

        return self.target.rotation + tank_rotate

    def getVelocity(self):
        tank_rotation = self.target.rotation
        cos_x = math.cos(math.radians(tank_rotation + 180))
        sin_x = math.sin(math.radians(tank_rotation + 180))
        return (self.speed * sin_x, self.speed * cos_x)

    def setGunPosition(self):
        self.target.Gun.position = self.target.position

    def setGunRotation(self, gun_turns_direction):
        self.target.Gun.gun_rotation += self.target.gun_rotation_speed * (gun_turns_direction)
        self.target.Gun.rotation = self.target.rotation + self.target.Gun.gun_rotation

    def addSpeed(self, moving_directions):
        if moving_directions:
            speed = self.speed + self.target.speed_acceleration * moving_directions

            if abs(speed) < self.target.max_speed:
                self.speed = speed

        else:
            if self.speed > 0:
                self.speed -= self.target.speed_acceleration
            elif self.speed < 0:
                self.speed += self.target.speed_acceleration