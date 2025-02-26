from vector import Vector
from constants import *
from entity import Entity
from sprites import VehicleSprites
from random import choice, randint
import pygame


class OtherVehicles(Entity):
    """
    Class representing a single vehicle that is not controlled by the user.
    """
    def __init__(self, node, name, sound, yard_loc):
        """
        Initializes a new car object. Uses entity as a superclass.

        Parameters:
            node (tuple): starting position of the car.
        """
        Entity.__init__(self, node)
        self.set_speed(20)
        self.direction_method = self.goal_direction

        # Gets correct sprite image
        self.sprites = VehicleSprites(self, name)

        self.time = 0
        self.timer = 0
        self.change_direction()
        self.collide_radius = 1

        self.send = False
        self.remove = False
        self.sound = sound
        self.yard_loc = yard_loc

    def change_direction(self):
        """
        Algorithm to control all other vehicles.
        Randomly decides whether to move horizontally or vertically, then resets movement timer
        based on the entity's position on the map.
        """

        # Reset timer
        self.timer = 0
        # Base is the base time - larger when position is at the outer edges of the map
        base = 0
        # Current position
        x, y = self.position.as_tuple()[0], self.position.as_tuple()[1]
        # Randomly chooses 1 - vertical movement or 2 - horizontal movement
        random_choice = choice([1, 2])

        # Vertical movement
        if random_choice == 1:
            x_goal = x
            # Move down
            if y <= 480:
                y_goal = 800
                if y <= 320:
                    base = 8
            # Move up
            else:
                y_goal = 200
                if y >= 640:
                    base = 8

        # Horizontal movement
        else:
            y_goal = y
            # Move right
            if x <= 480:
                x_goal = 960
                if x <= 240:
                    base = 8
            # Move left
            else:
                x_goal = 0
                if x >= 720:
                    base = 8

        # Time limit for direction - base plus a random number of seconds
        self.time = base + randint(6, 12)
        self.goal = Vector(x_goal, y_goal)

    def send_truck(self):
        """
        Function that sends all trucks to the Edmonton Global yard.
        """
        x = self.yard_loc[0][0] * 40
        y = self.yard_loc[0][1] * 40
        self.goal = Vector(x, y)

        dist = self.position - self.goal
        dist_squared = dist.magnitude_squared()

        if dist_squared <= 40 ** 2:
            self.remove = True
            pygame.mixer.Sound.play(self.sound)

    def update(self, dt):
        """
        Updates our vehicle object once per frame.

        Parameters:
            dt (float) : number of seconds since the previous update
        """

        if self.send:
            self.send_truck()
        else:
            self.timer += dt
            if self.timer >= self.time:
                self.change_direction()

        self.sprites.update()
        Entity.update(self, dt)

class VehicleGroup:
    """
    Class to hold all other vehicle objects (controlled by modes, not user)
    """
    def __init__(self):
        """
        Initializes a list that will store our vehicle objects.
        """
        self.vehicles = []
        self.vehicle_types = []

    def send_trucks(self):
        """
        Function to send all trucks to next city
        """
        for vehicle in self.vehicles:
            if vehicle.sprites.name is CONV_TRUCK:
                vehicle.send = True

    def update(self, dt):
        """
        Updates our object once per frame.

        Parameters:
            dt (float) : number of seconds since the previous update
        """
        self.vehicle_types = []
        for vehicle in self.vehicles:
            vehicle.update(dt)
            if not vehicle.send:
                self.vehicle_types.append(vehicle.sprites.name)

    def hide(self):
        """
        Hides all vehicle objects.
        """
        for vehicle in self.vehicles:
            vehicle.visible = False

    def show(self):
        """
        Shows all vehicle objects.
        """
        for vehicle in self.vehicles:
            vehicle.visible = True

    def draw(self, screen):
        """
        Draws our vehicle objects on the game screen.

        Parameters:
            screen (object): pygame surface to draw on
        """
        for vehicle in self.vehicles:
            vehicle.draw(screen)
