import math


class Vector(object):
    """
    Class representing vectors in our game. Stores position information.
    """
    def __init__(self, x=0, y=0):
        """
        Initializes a new vector with x and y positions.
        Parameters:
            x (int): horizontal value
            y (int): vertical value
        """
        self.x = x
        self.y = y
        self.thresh = 0.000001

    def __add__(self, other):

        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __div__(self, scalar):
        if scalar != 0:
            return Vector(self.x / float(scalar), self.y / float(scalar))
        return None

    def __truediv__(self, scalar):
        return self.__div__(scalar)

    def __eq__(self, other):
        if abs(self.x - other.x) < self.thresh:
            if abs(self.y - other.y) < self.thresh:
                return True
        return False

    def magnitude_squared(self):
        """
        Calculates and returns the squared magnitude of our vector.
        Used during movement functions.
        """
        return self.x ** 2 + self.y ** 2

    def magnitude(self):
        """
        Calculates and returns the length of our vector.
        """
        return math.sqrt(self.magnitude_squared())

    def copy(self):
        """
        Creates a new instance of the vector by returning its values.
        """
        return Vector(self.x, self.y)

    def as_tuple(self):
        """
        Returns the vector as a tuple.
        """
        return self.x, self.y

    def as_int(self):
        """
        Returns the vector as a tuple, with the coordinates as integers.
        """
        return int(self.x), int(self.y)

    # def __str__(self):
    #     return "<" + str(self.x) + ", " + str(self.y) + ">"
