import math

from app.math.vector import Vector

class SimulationConfig:
  DEFAULTS = {
    'simulation_fps': 1000,
    'balls_number': 10,
    'ball_radius': 10,
    'ball_velocity': Vector.from_polar(100, math.radians(30)),
    'ball_acceleration': Vector(0, 0)
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

