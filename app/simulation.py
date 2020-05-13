import math
import random
from app.point import Point
from app.vector import Vector
from app.rectangle import Rectangle
from app.ball import DrawableBall

def random_color():
  r = random.randint(20, 240)
  g = random.randint(20, 240)
  b = random.randint(20, 240)
  return (r, g, b)

class Simulation:
  def __init__(self, balls_number, width, height, radius):
    self.balls_number = balls_number
    self.width = width
    self.height = height
    self.radius = radius

    self.scene = Rectangle(0, 0, width, height)

    n = int(math.sqrt(balls_number))

    self.balls = []
    for index in range(balls_number):
      y = int(index / n)
      x = index % n

      self.balls.append(DrawableBall(
        Point(radius * 2 + x * (width / n), radius * 2 + y * (height / n)),
        radius,
        Vector(0, 0),
        random_color()
      ))
    
    self.balls[0].velocity = Vector.from_polar(1000, math.radians(30))
  
  def update(self, delta_time):
    for ball in self.balls:
      ball.update(delta_time)
    
    for ballIndex, ball in enumerate(self.balls):
      for other in self.balls[ballIndex + 1:]:
        if ball.is_collision_with_ball(other):
          ball.bounce_off_of_ball(other)
    
    for ball in self.balls:
      if ball.is_collision_with_wall(self.scene):
        ball.bounce_off_of_wall(self.scene)
      

  def draw(self, surface):
    for ball in self.balls:
      ball.draw(surface)
