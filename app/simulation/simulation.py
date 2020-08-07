import math
import random
from datetime import datetime
from collections import deque

from app.math.point import Point
from app.math.rectangle import Rectangle
from app.math.vector import Vector
from app.simulation.ball import Ball, TrackedBall
from app.simulation.frame import SimulationFrame
from app.config import SimulationConfig
from app.color import Color

from app.simulation.generator import FrameGenerator
from app.simulation.file import FrameFile


class Simulation:
    """
    This class is a main simulation manager
    """

    def __init__(self, config):
        self.scene_rectangle = Rectangle(
            0, 0, config['width'], config['height'])
        self.config = config

        initial_frame = FrameGenerator(config).generate()

        if self.config['save_simulation']:
            FrameFile(self.__generate_simulation_filename()
                      ).write(initial_frame)

        self.frames = deque([initial_frame])

    def generate_next_frame(self):
        delta_time = 1 / self.config['simulation_fps']
        last_frame = self.frames[-1]
        self.frames.append(last_frame.after(delta_time))

    def frames_left(self):
        return len(self.frames)

    def any_frames_left(self):
        return self.frames_left() != 0

    def pop_frame(self):
        return self.frames.popleft()

    def __generate_simulation_filename(self):
        time_string = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        extension = 'sim'
        return f'{time_string}.{extension}'
