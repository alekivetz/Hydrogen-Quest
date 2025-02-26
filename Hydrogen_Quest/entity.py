from vector import Vector
from constants import *


class Entity:
    """
    Super class for all vehicle, car, power up, and obstacle objects.
    """
    def __init__(self, node):
        """
        Initializes a new entity object.

        Parameters:
             node (object): starting node of the entity
        """
        self.directions = {
            UP: Vector(0, -1),
            DOWN: Vector(0, 1),
            LEFT: Vector(-1, 0),
            RIGHT: Vector(1, 0),
            STOP: Vector()
        }
        self.direction = STOP
        self.set_start_node(node)
        self.goal = None

        self.set_speed(60)
        self.collide_radius = 5

        self.visible = True
        self.image = None

    def set_start_node(self, node):
        """
        Sets the starting node of the entity.

        Parameters:
             node (object): starting node of the entity
        """
        self.node = node
        self.start_node = node
        self.target = node
        self.set_position()

    def set_position(self):
        """
        Sets the entity position to that of the given node.
        """
        self.position = self.node.position.copy()

    def valid_direction(self, direction):
        """
        Returns true if there is a node the entity can travel to in the given direction.

        Parameters:
            direction (int): integer representing up, down, left, or right
        """
        if direction is not STOP:
            if self.node.neighbours[direction] is not None:
                return True
        return False

    def get_new_target(self, direction):
        """
        Checks whether there is a node in the given direction.
        If so, send the entity to that node.

        Parameters:
            direction (int): integer representing up, down, left, or right
        """
        if self.valid_direction(direction):
            if self.node.neighbours[direction] is not None:
                return self.node.neighbours[direction]
        return self.node

    def overshot_target(self):
        """
        Checks to see if an entity has overshot their target node.
        Creates two vectors:
            the first is the distance between the goal node and the initial node
            the second is the distance between the entity and the initial node
        Compares their magnitudes and returns true or false accordingly.
        """
        if self.target is not None:
            vec1 = self.target.position - self.node.position
            vec2 = self.position - self.node.position
            node2target = vec1.magnitude_squared()
            node2self = vec2.magnitude_squared()
            return node2self >= node2target
        return False

    def reverse_direction(self):
        """
        Reverses the direction of the entity if a dead end has been hit.
        """
        self.direction *= -1
        temp = self.node
        self.node = self.target
        self.target = temp

    def opposite_direction(self, direction):
        """
        Checks if input direction is opposite to the current direction. Returns true if so.

        Parameters:
            direction (int): integer representing up, down, left, or right
        """
        if direction is not STOP:
            if direction == self.direction * -1:
                return True
        return False

    def set_speed(self, speed):
        """
        Sets the speed of the entity based on the size of our map.

        Parameters:
            speed (int): given speed
        """
        self.speed = speed * TILE_WIDTH / 16

    def update(self, dt):
        """
        Updates the vehicle object once per frame.

        Parameters:
            dt (float) : number of seconds since the previous update
        """
        # Move entity position
        self.position += self.directions[self.direction] * self.speed * dt

        # Check if entity overshot target
        if self.overshot_target():
            # Gets possible directions for entity to move, and chooses a random one
            self.node = self.target
            directions = self.valid_directions()
            direction = self.direction_method(directions)

            # Get a new target node in that direction
            self.target = self.get_new_target(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.get_new_target(self.direction)

            self.set_position()

    def valid_directions(self):
        """
        Creates a list of valid directions the entity can move in, based on node locations
        from calling valid_direction.
        Returns the list.
        """
        directions = []
        for key in [UP, DOWN, LEFT, RIGHT]:
            if self.valid_direction(key):
                if key != self.direction * -1:
                    directions.append(key)
        if len(directions) == 0:
            directions.append(self.direction * -1)
        return directions

    def goal_direction(self, directions):
        """
        Calculates the distance from the entity to the goal for each direction in a given list.
        Returns the direction with the smallest distance.

        Parameters:
            directions (list): a list of valid directions
        """
        distances = []
        for direction in directions:
            vec = self.node.position + self.directions[direction] * TILE_WIDTH - self.goal
            distances.append(vec.magnitude_squared())
        index = distances.index(min(distances))
        return directions[index]

    def draw(self, screen):
        """
        Draws the entity to the screen.

        Parameters:
            screen (object): pygame surface to draw on
        """
        if self.visible:
            screen.blit(self.image, self.position.as_tuple())
