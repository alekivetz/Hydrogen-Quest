import pygame
from pygame.locals import *
from constants import *
from entity import Entity
from sprites import VehicleSprites


class MyVehicle(Entity):
    """
    Class for vehicle controlled by the user.
    """
    def __init__(self, node):
        """
        Initializes the vehicle object. Uses entity as a superclass.

        Parameters:
            node (tuple): starting position of the car.
        """
        Entity.__init__(self, node)
        self.direction = STOP
        self.timer = 0
        self.sprites = VehicleSprites(self, name=MY_VEHICLE)

    def get_valid_key(self):
        """
        Detects when a user presses a key, and returns the correct value.
        If no key is being pressed, returns stop.
        """
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP]:
            return UP
        if key_pressed[K_DOWN]:
            return DOWN
        if key_pressed[K_LEFT]:
            return LEFT
        if key_pressed[K_RIGHT]:
            return RIGHT
        return STOP

    def update(self, dt):
        """
        Updates our vehicle object once per frame.

        Parameters:
            dt (float) : number of seconds since the previous update
        """

        # Update sprite image
        self.sprites.update()

        # Check for key presses and move the vehicle
        self.position += self.directions[self.direction] * self.speed * dt
        direction = self.get_valid_key()

        # Check if vehicle overshot their target
        if self.overshot_target():
            self.node = self.target
            # Gets a new valid direction for the vehicle to move
            self.target = self.get_new_target(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.get_new_target(self.direction)
            # Target has been reached, stop vehicle
            if self.target is self.node:
                self.direction = STOP
            self.set_position()
        else:
            # Reverse direction
            if self.opposite_direction(direction):
                self.reverse_direction()

        # Speed up vehicle if penalty is over
        self.timer += dt
        if self.timer >= 6:
            self.set_speed(60)

    def collision(self, other):
        """
        Checks for collisions between the vehicle and other entities.
        If the distance between the objects is less than the collision radius, return True.

        Parameters:
            other (entity): the other entity to be compared
        """
        dist = self.position - other.position
        dist_squared = dist.magnitude_squared()
        rad_squared = (self.collide_radius + other.collide_radius) ** 2
        if dist_squared <= rad_squared:
            return True
        return None



