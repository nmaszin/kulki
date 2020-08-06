from collections import deque

from app.math.point import Point
from app.math.vector import Vector
from app.math.rectangle import Rectangle
from app.math.matrix import TransformationMatrix
from app.graphics.circle import Circle

class Ball:
  """
  Mathematical model of ball
  This class handle move and collisions with wall and other objects
  """

  def __init__(self, position, radius, velocity, acceleration):
    self.position = position
    self.radius = radius
    self.velocity = velocity
    self.acceleration = acceleration

    self.track_length = 0
  
  def __eq__(self, other):
    return self.position == other.position and self.velocity == other.velocity and self.radius == other.radius

  def is_collision_with_ball(self, ball):
    """
    Returns True if collision between two balls has ocurred
    """
    distance = self.position.distance(ball.position)
    return distance <= self.radius + ball.radius
  
  def is_collision_with_wall(self, scene):
    """
    Returns True if collision between ball and wall has ocurred
    Wall is a border of scene rectangle
    """
    return not self.ball_possible_centers(scene).contains(self.position)
  
  def bounce_off_of_ball(self, ball):
    """
    Handle ball bouncing off of another ball
    Does not return anything
    """
    vector_between_centers = Vector(
      ball.position.x - self.position.x,
      ball.position.y - self.position.y
    )

    vector_x = vector_between_centers.norm()
    vector_y = vector_between_centers.ortogonal().norm()
    matrix = TransformationMatrix(vector_x, vector_y)

    self_velocity_transformed = matrix.to_base(self.velocity)
    ball_velocity_transformed = matrix.to_base(ball.velocity)

    # First coordinates exchange
    # Second coordinate is preserved
    temp = self_velocity_transformed.x 
    self_velocity_transformed.x = ball_velocity_transformed.x
    ball_velocity_transformed.x = temp

    self.velocity = matrix.from_base(self_velocity_transformed)
    ball.velocity = matrix.from_base(ball_velocity_transformed)

  def bounce_off_of_wall(self, scene):
    """
    Handle ball bouncing off of walls
    Does not return anything
    """
    possible_centers = self.ball_possible_centers(scene)

    if self.position.x < possible_centers.left():
      self.velocity.x *= -1
    elif self.position.x > possible_centers.right():
      self.velocity.x *= -1
    
    if self.position.y < possible_centers.top():
      self.velocity.y *= -1
    elif self.position.y > possible_centers.bottom():
      self.velocity.y *= -1


  def ball_possible_centers(self, scene):
    """
    Returns a rectangle that describes area
    consisting of all possible points (centers of ball)
    which ball is able to have
    """
    return Rectangle(
      x=scene.x + self.radius + 1,
      y=scene.y + self.radius + 1,
      width=scene.width - 2 * self.radius - 2,
      height=scene.height - 2 * self.radius - 2,
    )

  def update(self, time_delta):
    """
    Updates position of the ball after time_delta seconds
    Does not return anything
    """
    velocity_displacement = self.acceleration * time_delta
    self.velocity += velocity_displacement

    displacement = self.velocity * time_delta
    self.track_length += abs(displacement)
    self.position = self.position.translate(displacement)

class TrackedBall(Ball):
  TRACK_SIZE = 100

  def __init__(self, position, radius, velocity, acceleration):
    super().__init__(position, radius, velocity, acceleration)
    self.previous_positions = deque([])
  
  def update(self, time_delta):
    self.previous_positions.append(self.position)
    super().update(time_delta)

    if len(self.previous_positions) > self.TRACK_SIZE:
      self.previous_positions.popleft()
