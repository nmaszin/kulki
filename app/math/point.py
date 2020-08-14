import math
import random

from app.math.vector import Vector


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def translate(self, vector):
        return Point(
            self.x + vector.x,
            self.y + vector.y
        )

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __repr__(self):
        return str(self)

    def __iter__(self):
        yield self.x
        yield self.y

    def serialize(self):
        return {
            'x': self.x,
            'y': self.y
        }

    @staticmethod
    def deserialize(data):
        return Point(
            data['x'],
            data['y']
        )
