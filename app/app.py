import pygame
from app.point import Point
from app.rectangle import Rectangle
from app.vector import Vector
from app.ball import DrawableBall

class App:
  WINDOW_TITLE = 'Kulki by N-Maszin'
  WINDOW_HEIGHT = 800
  WINDOW_WIDTH = 800
  WINDOW_BACKGROUND = (240, 240, 240)
  FPS = 60

  running = False

  def __init__(self):
    pygame.init()
    pygame.display.set_caption(self.WINDOW_TITLE)
    self.surface = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
    self.surface.fill(self.WINDOW_BACKGROUND)

    self.balls = []
    for y in range(10):
      for x in range(10):
        self.balls.append(DrawableBall(Point(110 + 60 * x, 110 + 60 * y), 10, Vector(200, 200)))
    
    for ball in self.balls:
      ball.draw(self.surface)

    self.UPDATE_WORLD = pygame.USEREVENT
    pygame.time.set_timer(self.UPDATE_WORLD, int(1000 / self.FPS))

    pygame.display.update()

  def run(self):
    self.running = True
    while self.running:
      for event in pygame.event.get():
        self.handle_event(event)

  def handle_event(self, event):
    if event.type == pygame.QUIT:
      self.running = False
    elif event.type == self.UPDATE_WORLD:
      scene = Rectangle(100, 100, self.WINDOW_WIDTH - 200, self.WINDOW_HEIGHT - 200)

      delta_time = 1 / self.FPS

      for ball in self.balls:
        ball.update(delta_time)

      for index in range(len(self.balls)):
        ball = self.balls[index]
        for other in self.balls[index + 1:]:
          if ball.is_collision_with_ball(other):
            ball.bounce_off_of_ball(other)
      
      for ball in self.balls:
        if ball.is_collision_with_wall(scene):
          ball.bounce_off_of_wall(scene)
      
      self.surface.fill(self.WINDOW_BACKGROUND)
      for index in range(len(self.balls)):
        ball = self.balls[index]
        if index == 3:
          ball.draw(self.surface, color=(0, 240, 0))
        else:
          ball.draw(self.surface)

      pygame.display.update()

app = App()
app.run()