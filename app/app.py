import pygame
import random

from app.math.rectangle import Rectangle
from app.math.vector import Vector
from app.simulation.simulation import Simulation
from app.simulation.config import SimulationConfig
from app.color import Color

class App:
  WINDOW_TITLE = 'Kulki by N-Maszin'
  WINDOW_ICON_PATH = 'assets/icon.png'
  WINDOW_HEIGHT = 600
  WINDOW_WIDTH = 600
  FPS = 60
  GENERATE_FPS = 600

  running = False
  paused = False

  def __init__(self):
    self.init_window()
    self.init_simulation()
    self.init_timers()

  def init_window(self):
    pygame.init()
    pygame.display.set_caption(self.WINDOW_TITLE)
    pygame.display.set_icon(pygame.image.load(self.WINDOW_ICON_PATH))
    self.surface = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
    self.surface.fill(Color.BACKGROUND)
    pygame.display.update()

  def init_simulation(self):
    self.simulation = Simulation(
      SimulationConfig({
        'balls_number': 10,
        'width': self.WINDOW_WIDTH,
        'height': self.WINDOW_HEIGHT
      })
    )

  def init_timers(self):
    self.GENERATE_FRAME_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(self.GENERATE_FRAME_EVENT, int(1000 / self.GENERATE_FPS))

    self.RENDER_FRAME_EVENT = pygame.USEREVENT
    pygame.time.set_timer(self.RENDER_FRAME_EVENT, int(1000 / self.FPS))

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
    elif event.type == self.RENDER_FRAME_EVENT and not self.paused:
      self.surface.fill(Color.BACKGROUND)
      self.simulation.draw_next_frame(self.surface)
      pygame.display.update()
    elif event.type == self.GENERATE_FRAME_EVENT:
      self.simulation.generate_next_frame()
