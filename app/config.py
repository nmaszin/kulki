import math
import random
import json
from multicon import Config

from app.math.vector import Vector
from app.json_file import JsonFile


class SimulationConfig(Config):
    DEFAULTS = {
        'width': 600,
        'height': 600,
        'fullscreen': False,
        'fps': 60,
        'engine_fps': 60,
        'exit_at_the_end_of_simulation': True,

        'collisions_precision': 1,
        'balls_radius': 10,
        'track_dots_radius': 2,

        'regular_balls_number': 10,
        'regular_balls_velocity': {
            'angle': [0, 360],
            'value': [0, 500]
        },
        'regular_balls_acceleration': {
            'angle': [0, 0],
            'value': [0, 0]
        },

        'tracked_balls_number': 1,
        'tracked_balls_velocity': {
            'angle': [0, 360],
            'value': [0, 500]
        },
        'tracked_balls_acceleration': {
            'angle': [0, 0],
            'value': [0, 0]
        },
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
