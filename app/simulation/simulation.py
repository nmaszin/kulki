import math
import random
from collections import deque

from app.math.point import Point
from app.math.rectangle import Rectangle
from app.math.vector import Vector
from app.simulation.ball import Ball, TrackedBall
from app.simulation.frame import SimulationFrame
from app.simulation.config import SimulationConfig
from app.color import Color

class Simulation:
  """
  This class is a main simulation manager
  """
  def __init__(self, config):
    self.scene_rectangle = Rectangle(0, 0, config['width'], config['height'])
    self.config = config

    positions = self.randomize_initial_balls_positions(
      self.scene_rectangle,
      config['balls_number'],
      config['ball_radius']
    )
    
    balls = []
    balls.append(TrackedBall(
      position=positions.pop(),
      radius=config['ball_radius'],
      velocity=config['ball_velocity'](),
      acceleration=config['ball_acceleration'](),
      collisions_precision=config['collisions_precision']
    ))

    for position in positions:
      balls.append(Ball(
        position=position,
        radius=config['ball_radius'],
        velocity=config['ball_velocity'](),
        acceleration=config['ball_acceleration'](),
        collisions_precision=config['collisions_precision']
      ))
    
    self.frames = deque([SimulationFrame(
      self.scene_rectangle,
      balls
    )])

  def generate_next_frame(self):
    delta_time = 1 / self.config['simulation_fps']
    last_frame = self.frames[-1]
    self.frames.append(last_frame.after(delta_time))
  
  def frames_left(self):
    return len(self.frames)
  
  def any_frames_left(self):
    return self.frames_left() != 0

  def pop_frame(self):
    return self.frames.popleft()
  
  @staticmethod
  def randomize_initial_balls_positions(scene_rectangle, balls_number, ball_radius):
    rows_number = columns_number = math.ceil(math.sqrt(balls_number))
    
    area_width = int(scene_rectangle.width / columns_number)
    area_height = int(scene_rectangle.height / rows_number)

    busy_areas = [[False] * columns_number for y in range(rows_number)]

    positions = []
    for _ in range(balls_number):
      while True:
        x = random.randint(0, columns_number - 1)
        y = random.randint(0, rows_number - 1)
        if not busy_areas[y][x]:
          busy_areas[y][x] = True
          break

      rect = Rectangle(
        scene_rectangle.x + area_width * x + ball_radius,
        scene_rectangle.y + area_height * y + ball_radius,
        area_width - 2 * ball_radius,
        area_height - 2 * ball_radius
      )
      
      positions.append(rect.random_point())
    
    return positions
