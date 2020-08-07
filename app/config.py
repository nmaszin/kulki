import math
import random

from app.math.vector import Vector


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
        'save_simulation': True,

        'simulation_fps': 60,
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
