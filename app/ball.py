import pygame
import pygame.gfxdraw
from app.point import Point
from app.vector import Vector
from app.rectangle import Rectangle
from app.matrix import TransformationMatrix

class Ball:
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
    return distance <= self.radius + ball.radius + 1
  
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

class DrawableBall(Ball):
  def __init__(self, position, radius, velocity, acceleration, color):
    super().__init__(position, radius, velocity, acceleration)
    self.color = color

  def draw(self, surface):
    pygame.gfxdraw.aacircle(
      surface,
      *tuple(self.position.coords_int()),
      self.radius,
      self.color
    )
    pygame.gfxdraw.filled_circle(
      surface,
      *tuple(self.position.coords_int()),
      self.radius,
      self.color
    )