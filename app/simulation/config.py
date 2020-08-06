import math
import random

from app.math.vector import Vector
from app.config import Config

class SimulationConfig(Config):
  DEFAULTS = {
    'simulation_fps': 60,
    'balls_number': 100,
    'ball_radius': 10,
    'ball_velocity': lambda: Vector.from_polar(500, math.radians(random.randint(0, 360))),
    'ball_acceleration': lambda: Vector(0, 0),
    'collisions_precision': 1
  }

  def __init__(self, config):
    super().__init__(self.DEFAULTS, config)
