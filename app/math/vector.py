import math


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def from_polar(r, phi):
        return Vector(
            r * math.cos(phi),
            r * math.sin(phi)
        )

    def __str__(self):
        return f'[{self.x}, {self.y}]'

    def __repr__(self):
        return str(self)

    def __add__(self, other):
        """
        Returns a vector which is a result of adding this vector to another
        """
        return Vector(
            self.x + other.x,
            self.y + other.y
        )

    def __sub__(self, other):
        """
        Returns a vector which is a result of substracting this vector by another
        """
        return Vector(
            self.x - other.x,
            self.y - other.y
        )

    def __mul__(self, scale):
        """
        Returns a vector which is a result of scalling current vector
        """
        return Vector(
            self.x * scale,
            self.y * scale
        )

    def __abs__(self):
        """
        Returns the magnitude of the vector
        """
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def dot(self, other):
        """
        Returns dot product of two vectors
        """
        return self.x * other.x + self.y * other.y

    def angle(self, other):
        """
        Returns value of degree between two vector
        The angle is returned in degrees
        """
        return math.degrees(
            math.acos(self.dot(other) / (abs(self) * abs(other)))
        )

    def ortogonal(self):
        """
        Returns a basic vector which is ortogonal to this vector
        """
        x = 1
        if self.y != 0:
            return Vector(
                x,
                -x * self.x / self.y
            )
        else:
            return Vector(
                self.y,
                self.x
            )

    def norm(self):
        """
        Returns a normed vector
        """
        scale = 1 / abs(self)
        return self * scale

    def serialize(self):
        return {
            'x': self.x,
            'y': self.y
        }

    @staticmethod
    def deserialize(data):
        return Vector(
            data['x'],
            data['y']
        )
