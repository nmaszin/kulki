import math
import random
from datetime import datetime
from collections import deque

from app.list import DoubleLinkedList
from app.config import SimulationConfig
from app.math.point import Point
from app.math.rectangle import Rectangle
from app.math.vector import Vector
from app.simulation.ball import Ball, TrackedBall
from app.simulation.frame import SimulationFrame
from app.simulation.generator import FrameGenerator
from app.graphics.color import Color


class Simulation:
    """
    Klasa stanowiąca główny menedżer symulacji
    """

    def __init__(self, config, initial_frame):
        """
        Konstruktor klasy. Przekazywane do niego są: konfiguracja oraz pierwsza klatka
        """

        self.scene_rectangle = Rectangle(
            0, 0, config['width'], config['height'])

        self.config = config
        self.initial_frame = initial_frame

        self.frames = DoubleLinkedList.from_list([initial_frame])
        self.current_frame_iterator = self.frames.iterator_first()
        self.frames_counter = 0

    def generate_next_frame(self):
        """
        Metoda, która generuje następną klatkę (bazując na ostatniej już wygenerowanej),
        a następnie dokleja ją na koniec listy
        """

        delta_time = 1 / self.config['engine_fps']
        self.frames.push_last(self.frames.last().after(delta_time))
        self.frames_counter += 1

    def at_first_frame(self):
        """
        Metoda zwraca True, jeżeli symulacja wskazuje na pierwszą klatkę
        """

        return not self.current_frame_iterator.has_previous()

    def at_last_frame(self):
        """
        Metoda zwraca True, jeżeli symulacja wskazuje na ostatnią klatkę
        """

        return not self.current_frame_iterator.has_next()

    def go_to_next_frame(self):
        """
        Metoda, dzięki której symulacja przechodzi do następnej klatki
        """

        self.current_frame_iterator = self.current_frame_iterator.next
        return self.current_frame_iterator.previous.value

    def go_to_previous_frame(self):
        """
        Metoda, dzięki której symulacja przechodzi do poprzedniej klatki
        """

        self.current_frame_iterator = self.current_frame_iterator.previous
        return self.current_frame_iterator.next.value

    def current_frame(self):
        """
        Metoda zwraca obecną klatkę
        """

        return self.current_frame_iterator.value

    def should_end(self):
        """
        Metoda zwraca True, jeżeli symulacja powinna się już zakończyć,
        czyli w przypadku gdy użytkowik ustawił opcję 'simulation_max_frames'
        w konfiguracji, i wygenerowano już tyle klatek, ile było trzeba
        """

        key = 'simulation_max_frames'
        return key in self.config and self.frames_counter >= self.config[key]

    def serialize(self):
        """
        Metoda która serializuje obiekt
        (konwertuje go do postaci, która jest bardziej przenośna; można ją np. zapisać do pliku)
        """

        return {
            'config': self.config.serialize(),
            'initial_frame': self.initial_frame.serialize()
        }

    @staticmethod
    def deserialize(data):
        """
        Metoda statyczna, która deserializuje obiekt (tworzy nowy obiekt,
        na podstawie zserializowanych danych)
        """

        return Simulation(
            SimulationConfig.deserialize(data['config']),
            SimulationFrame.deserialize(data['initial_frame'])
        )
