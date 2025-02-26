from random import randint
from nodes import Node
from constants import *
from sprites import Spritesheet


class FuelStations:
    """
    A class to represent the spawned fuel stations.
    """
    def __init__(self, nodes, all_open):
        """
        Initializes the fuel station objects.

        Parameters:
            all_open (list): list containing all grass locations where the station can be spawned

        """
        self.sprite = Spritesheet().get_image(5, 0, TILE_WIDTH, TILE_HEIGHT)

        self.nodes = nodes
        self.open_locations = all_open
        self.occupied_locations = []

        self.position = None
        # List of fuel station positions
        self.positions = []

    def add_station(self):
        """
        Adds a fuel station to the list of fuel station positions.
        """
        # Get random position
        position = self.open_locations[randint(0, len(self.open_locations) - 1)]

        if position not in self.occupied_locations:
            x, y = position[0], position[1]
            # Construct a node of the position to check for collisions later
            x_pixel, y_pixel = self.nodes.construct_key(x, y)
            temp = Node(x_pixel, y_pixel)
            self.nodes.nodes_dict[(x, y)] = temp
            self.position = temp.position.copy()
            self.occupied_locations.append((x, y))
            self.positions.append(self.position)

    def draw(self, background):
        """
        Draws the fuel station on the map.

        Parameters:
            background (object): the background to be drawn on
        """
        for position in self.occupied_locations:
            x, y = position[0], position[1]
            background.blit(self.sprite, (x * TILE_WIDTH, y * TILE_HEIGHT))

        return background

