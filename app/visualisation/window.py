import pygame
import random
import threading

from app.math.rectangle import Rectangle
from app.math.vector import Vector
from app.simulation.simulation import Simulation
from app.config import SimulationConfig
from app.visualisation.frame import DrawableFrame
from app.graphics.color import Color
from app.simulation.file import SimulationFile

class VisualisationWindow:
    WINDOW_TITLE = 'Kulki by N-Maszin'
    WINDOW_ICON_PATH = 'assets/icon.png'

    running = False
    paused = False

    def __init__(self, simulation):
        self.simulation = simulation
        self.simulation_saved = False
        self.simulation_backward = False

        self.init_window()
        self.init_timers()

    def init_window(self):
        pygame.init()
        pygame.display.set_caption(self.WINDOW_TITLE)
        pygame.display.set_icon(pygame.image.load(self.WINDOW_ICON_PATH))
        self.surface = pygame.display.set_mode(
            (self.simulation.config['width'], self.simulation.config['height']))
        self.surface.fill(Color.BACKGROUND)
        pygame.display.update()

    def init_timers(self):
        self.GENERATE_FRAME_EVENT = pygame.USEREVENT
        pygame.time.set_timer(self.GENERATE_FRAME_EVENT,
                              int(1000 / self.simulation.config['engine_fps']))

        self.RENDER_FRAME_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.RENDER_FRAME_EVENT, int(1000 / self.simulation.config['fps']))

    def run(self):
        try:
            self.running = True
            while self.running:
                for event in pygame.event.get():
                    self.handle_event(event)
        except KeyboardInterrupt:
            pass

        return self.simulation.current_frame()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.key == pygame.K_p:
                self.paused = not self.paused
            elif event.key == pygame.K_s and not self.simulation_saved:
                FrameFile(FrameFile.generate_name()).write(self.simulation.frames[0])
                self.simulation_saved = True
                print('Saved successfully')
            elif event.key == pygame.K_b:
                self.simulation_backward = True
            elif event.key == pygame.K_f:
                self.simulation_backward = False

        elif event.type == self.RENDER_FRAME_EVENT and not self.paused:
            def obtain_and_render_frame(obtainer):
                self.surface.fill(Color.BACKGROUND)
                frame = obtainer()
                DrawableFrame(frame, self.simulation.config).draw(self.surface)
                pygame.display.update()

            if self.simulation_backward and not self.simulation.at_first_frame():
                obtain_and_render_frame(self.simulation.go_to_previous_frame)
            elif not self.simulation_backward and not self.simulation.at_last_frame():
                obtain_and_render_frame(self.simulation.go_to_next_frame)
            
            if self.simulation.should_end() and self.simulation.config['exit_at_the_end_of_simulation']:
                self.running = False

        elif event.type == self.GENERATE_FRAME_EVENT and not self.simulation_backward and not self.simulation.should_end():
            threading.Thread(target=self.simulation.generate_next_frame).start()
