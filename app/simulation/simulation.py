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
from app.graphics.color import Color

from app.simulation.generator import FrameGenerator
from app.simulation.file import FrameFile

from app.list import DoubleLinkedList


class Simulation:
    """
    This class is a main simulation manager
    """

    def __init__(self, config, initial_frame):
        self.scene_rectangle = Rectangle(
            0, 0, config['width'], config['height'])
        
        self.config = config
        self.frames = DoubleLinkedList.from_list([initial_frame])
        self.current_frame_iterator = self.frames.iterator_first()

    def generate_next_frame(self):
        delta_time = 1 / self.config['engine_fps']
        self.frames.push_last(self.frames.last().after(delta_time))

    def is_first_frame(self):
        return not self.current_frame_iterator.has_previous()
    
    def is_last_frame(self):
        return not self.current_frame_iterator.has_next()

    def next_frame(self):
        self.current_frame_iterator = self.current_frame_iterator.next
        return self.current_frame_iterator.previous.value
    
    def previous_frame(self):
        self.current_frame_iterator = self.current_frame_iterator.previous
        return self.current_frame_iterator.next.value

