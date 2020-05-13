import pygame
from app.simulation import Simulation

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

    self.simulation = Simulation(64, self.WINDOW_WIDTH, self.WINDOW_HEIGHT, 15)
    self.simulation.draw(self.surface)
    pygame.display.update()

    self.UPDATE_SIMULATION = pygame.USEREVENT
    pygame.time.set_timer(self.UPDATE_SIMULATION, int(1000 / self.FPS))

  def run(self):
    self.running = True
    while self.running:
      for event in pygame.event.get():
        self.handle_event(event)
    
    print('Najkrótsza droga przebyta przez jedną kulkę:', min(map(lambda ball: ball.track_length, self.simulation.balls)))
    print('Najdłuższa droga przebyta przez jedną kulkę:', max(map(lambda ball: ball.track_length, self.simulation.balls)))

  def handle_event(self, event):
    if event.type == pygame.QUIT:
      self.running = False
    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        self.running = False
    elif event.type == self.UPDATE_SIMULATION:
      self.simulation.update(1 / self.FPS)
      
      self.surface.fill(self.WINDOW_BACKGROUND)
      self.simulation.draw(self.surface)
      pygame.display.update()
