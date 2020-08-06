import copy

class SimulationFrame:
  def __init__(self, scene, balls):
    self.scene = scene
    self.balls = balls
  
  def after(self, delta_time):
    """
    This method is responsible for generating the next frame
    that will occur after some delta_time
    """
    balls = copy.deepcopy(self.balls)
    
    for ball in balls:
      ball.update(delta_time)
    
    for ballIndex, ball in enumerate(balls):
      for other in balls[ballIndex + 1:]:
        if ball.is_collision_with_ball(other):
          ball.bounce_off_of_ball(other)
    
    for ball in balls:
      if ball.is_collision_with_wall(self.scene):
        ball.bounce_off_of_wall(self.scene)
    
    return SimulationFrame(
      self.scene,
      balls
    )
