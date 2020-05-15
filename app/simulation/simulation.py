import math
from collections import deque

from app.math.point import Point
from app.math.vector import Vector
from app.simulation.ball import DrawableBall, TrackedBall
from app.simulation.frame import SimulationFrame
from app.simulation.config import SimulationConfig
from app.color import Color

class Simulation:
  """
  This class is a main simulation manager
  """
  def __init__(self, scene, config):
    self.scene = scene
    self.config = config

    balls = []
    balls.append(TrackedBall(
      position=scene.random_point(),
      radius=config.get('ball_radius'),
      velocity=config.get('ball_velocity'),
      acceleration=config.get('ball_acceleration'),
      color=Color.random(),
      track_color=Color.random()
    ))

    for _ in range(config.get('balls_number') - 1):
      balls.append(DrawableBall(
        position=scene.random_point(),
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
