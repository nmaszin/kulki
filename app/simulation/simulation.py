import math
import random
from collections import deque

from app.math.point import Point
from app.math.rectangle import Rectangle
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

    positions = self.randomize_initial_balls_positions(
      scene,
      config.get('balls_number'),
      config.get('ball_radius')
    )
    
    balls = []
    balls.append(TrackedBall(
      position=positions.pop(),
      radius=config.get('ball_radius'),
      velocity=config.get('ball_velocity')(),
      acceleration=config.get('ball_acceleration')(),
      color=Color.TRACKED_BALL,
      track_color=Color.TRACK
    ))

    for position in positions:
      balls.append(DrawableBall(
        position=position,
        radius=config.get('ball_radius'),
        velocity=config.get('ball_velocity')(),
        acceleration=config.get('ball_acceleration')(),
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
  
  @staticmethod
  def randomize_initial_balls_positions(scene, balls_number, ball_radius):
    rows_number = columns_number = math.ceil(math.sqrt(balls_number))
    
    area_width = int(scene.width / columns_number)
    area_height = int(scene.height / rows_number)

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
        scene.x + area_width * x + ball_radius,
        scene.y + area_height * y + ball_radius,
        area_width - 2 * ball_radius,
        area_height - 2 * ball_radius
      )
      
      positions.append(rect.random_point())
    
    return positions

