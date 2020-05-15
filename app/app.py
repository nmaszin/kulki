import pygame
import random

from app.math.rectangle import Rectangle
from app.math.vector import Vector
from app.simulation.simulation import Simulation
from app.simulation.config import SimulationConfig
from app.color import Color

class App:
  WINDOW_TITLE = 'Kulki by N-Maszin'
  WINDOW_HEIGHT = 800
  WINDOW_WIDTH = 800
  FPS = 60

  running = False
  paused = False

  def __init__(self):
    pygame.init()
    pygame.display.set_caption(self.WINDOW_TITLE)
    self.surface = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
    self.surface.fill(Color.BACKGROUND)

    self.scene = Rectangle(0, 0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

    self.simulation = Simulation(
      self.scene,
      SimulationConfig({}) # default config
    )

    self.RENDER_FRAME = pygame.USEREVENT
    pygame.time.set_timer(self.RENDER_FRAME, int(1000 / self.FPS))

    pygame.display.update()

  def run(self):
    self.running = True
    while self.running:
      for event in pygame.event.get():
        self.handle_event(event)

  def handle_event(self, event):
    if event.type == pygame.QUIT:
      self.running = False
    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        self.running = False
      elif event.key == pygame.K_p:
        self.paused = not self.paused
      
    elif event.type == self.RENDER_FRAME and not self.paused:
      self.simulation.generate_next_frame()
      self.surface.fill(Color.BACKGROUND)
      self.simulation.draw_next_frame(self.surface)
      pygame.display.update()
