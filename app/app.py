import pygame
import random
import threading

from app.math.rectangle import Rectangle
from app.math.vector import Vector
from app.simulation.simulation import Simulation
from app.config import SimulationConfig
from app.visualisation.frame import DrawableFrame
from app.graphics.color import Color
from app.simulation.file import FrameFile

class App:
    WINDOW_TITLE = 'Kulki by N-Maszin'
    WINDOW_ICON_PATH = 'assets/icon.png'

    BUFFERED_FRAMES_NUMBER = 10

    running = False
    paused = False

    def __init__(self, config, initial_frame):
        self.config = config
        self.initial_frame = initial_frame
        self.simulation_saved = False

        self.init_window()
        self.init_simulation()
        self.init_timers()

    def init_window(self):
        pygame.init()
        pygame.display.set_caption(self.WINDOW_TITLE)
        pygame.display.set_icon(pygame.image.load(self.WINDOW_ICON_PATH))
        self.surface = pygame.display.set_mode(
            (self.config['width'], self.config['height']))
        self.surface.fill(Color.BACKGROUND)
        pygame.display.update()

    def init_simulation(self):
        self.simulation = Simulation(self.config, self.initial_frame)

    def init_timers(self):
        self.GENERATE_FRAME_EVENT = pygame.USEREVENT
        pygame.time.set_timer(self.GENERATE_FRAME_EVENT,
                              int(1000 / self.config['engine_fps']))

        self.RENDER_FRAME_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.RENDER_FRAME_EVENT, int(1000 / self.config['fps']))

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
            elif event.key == pygame.K_s and not self.simulation_saved:
                FrameFile(FrameFile.generate_name()).write(self.initial_frame)
                self.simulation_saved = True
                print('Saved successfully')
                

        elif event.type == self.RENDER_FRAME_EVENT and not self.paused and self.simulation.frames_left() > self.BUFFERED_FRAMES_NUMBER:
            self.surface.fill(Color.BACKGROUND)
            frame = self.simulation.pop_frame()
            DrawableFrame(frame, self.config).draw(self.surface)
            pygame.display.update()
        elif event.type == self.GENERATE_FRAME_EVENT:
            t = threading.Thread(
                target=self.simulation.generate_next_frame
            )
            t.start()
