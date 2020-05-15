import math
from collections import deque

from app.point import Point
from app.vector import Vector
from app.ball import DrawableBall
from app.color import Color
from app.frame import SimulationFrame

class SimulationConfig:
  DEFAULTS = {
    'simulation_fps': 1000,
    'balls_number': 100,
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


class Simulation:
  def __init__(self, scene, config):
    self.scene = scene
    self.config = config

    balls = []
    for _ in range(config.get('balls_number')):
      balls.append(DrawableBall(
        position=Point(200, 200),
        radius=config.get('ball_radius'),
        velocity=config.get('ball_velocity'),
        acceleration=config.get('ball_acceleration'),
        color=Color.BALL
      ))
    
    self.frames = deque([SimulationFrame(
      self.scene,
      balls
    )])

  def generate_next_frame(self):
    delta_time = 1 / self.config.get('simulation_fps')
    last_frame = self.frames[-1]
    self.frames.append(last_frame.after(delta_time))
  
  def any_frames_left(self):
    return len(self.frames) != 0

  def draw_next_frame(self, surface):
    frame = self.frames.popleft()
    frame.draw(surface)
