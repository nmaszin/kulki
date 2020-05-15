import math
import random

from app.math.vector import Vector

class SimulationConfig:
  DEFAULTS = {
    'simulation_fps': 60,
    'balls_number': 100,
    'ball_radius': 10,
    'ball_velocity': lambda: Vector.from_polar(500, math.radians(random.randint(0, 360))),
    'ball_acceleration': lambda: Vector(0, 0)
  }

  def __init__(self, config):
    self.config = config
  
  def get(self, property):
    if property in self.config:
      return self.config[property]
    
    if property in self.DEFAULTS:
      return self.DEFAULTS[property]
  
  def set(self, property, value):
    self.config[property] = value

