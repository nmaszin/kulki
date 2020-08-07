import math
import random

from app.math.vector import Vector
from app.config import Config


class SimulationConfig(Config):
    DEFAULTS = {
        'save_simulation': True,

        'simulation_fps': 60,
        'collisions_precision': 5,
        'balls_radius': 10,

        'regular_balls_number': 10,
        'regular_balls_velocity': lambda: Vector.from_polar(500, math.radians(random.randint(0, 360))),
        'regular_balls_acceleration': lambda: Vector(0, 0),

        'tracked_balls_number': 1,
        'tracked_balls_velocity': lambda: Vector.from_polar(300, math.radians(random.randint(0, 90))),
        'tracked_balls_acceleration': lambda: Vector(0, 0),
    }

    def __init__(self, config):
        super().__init__(self.DEFAULTS, config)
