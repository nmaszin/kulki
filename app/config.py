import math
import random
import json

from app.math.vector import Vector
from app.json_file import JsonFile

class Config:
    def __init__(self, default, custom):
        self.default = default
        self.custom = custom

    def __contains__(self, property):
        return property in self.custom or property in self.default

    def __getitem__(self, property):
        return self.custom.get(property, self.default.get(property, None))

    def __setitem__(self, property, value):
        self.custom[property] = value

    def __delitem__(self, property):
        del self.custom[property]

    def clear(self):
        self.custom.clear()

    def all(self):
        return {**self.default, **self.custom}


class SimulationConfig(Config):
    DEFAULTS = {
        'width': 600,
        'height': 600,
        'fps': 60,
        'engine_fps': 60,
        'exit_at_the_end_of_simulation': True,

        'collisions_precision': 1,
        'balls_radius': 10,
        'track_dots_radius': 2,

        'regular_balls_number': 10,
        'regular_balls_velocity': lambda: Vector.from_polar(500, math.radians(random.randint(0, 360))),
        'regular_balls_acceleration': lambda: Vector(0, 0),

        'tracked_balls_number': 1,
        'tracked_balls_velocity': lambda: Vector.from_polar(300, math.radians(random.randint(0, 90))),
        'tracked_balls_acceleration': lambda: Vector(0, 0),
    }

    def __init__(self, config):
        super().__init__(self.DEFAULTS, config)

    def serialize(self):
        return self.custom
    
    @staticmethod
    def deserialize(data):
        return SimulationConfig(data)


class ConfigObtainer:
    def __init__(self, path=None):
        self.path = path
    
    def obtain(self):
        if self.path is None:
            custom_config = {}
        else:
            custom_config = JsonFile(self.path).read()
        
        return SimulationConfig(custom_config)