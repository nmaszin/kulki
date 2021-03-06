import math
import random

from app.math.vector import Vector
from app.math.rectangle import Rectangle
from app.simulation.frame import SimulationFrame
from app.simulation.ball import Ball, TrackedBall


class FrameGenerator:
    """
    Klasa, która zajmuje się generowaniem inicjalnej klatki,
    na podstawie konfiguracji symulacji.

    Konfiguracja ta zawiera między innymi informacje na temat
    ilości kulek, ich rozmiaru, ich minimalnych/maksymalnych prędkości itd.
    """

    def __init__(self, config):
        """
        Konstruktor klasy. Jako argument przekazywana jest konfiguracja symulacji.
        """

        self.config = config
        self.scene_rectangle = Rectangle(
            0, 0, self.config['width'], self.config['height'])

    def generate(self):
        """
        Metoda generująca klatkę i zwracająca ją
        """

        positions = self.__randomize_positions()

        balls = []
        for _ in range(self.config['tracked_balls_number']):
            balls.append(TrackedBall(
                position=positions.pop(),
                radius=self.config['balls_radius'],
                velocity=Vector.generate(self.config['tracked_balls_velocity']),
                acceleration=Vector.generate(self.config['tracked_balls_acceleration']),
                collisions_precision=self.config['collisions_precision']
            ))

        for _ in range(self.config['regular_balls_number']):
            balls.append(Ball(
                position=positions.pop(),
                radius=self.config['balls_radius'],
                velocity=Vector.generate(self.config['regular_balls_velocity']),
                acceleration=Vector.generate(self.config['regular_balls_acceleration']),
                collisions_precision=self.config['collisions_precision']
            ))

        return SimulationFrame(
            self.scene_rectangle,
            balls
        )

    def __randomize_positions(self):
        """
        Metoda, która (w nieco chałupniczy sposób) generuje pozycje dla kulek,
        ale w ten sposób, żeby te się w żaden sposób nie pokrywały.

        Wygenerowane pozycje są zwracane w postaci listy punktów
        (lista obiektów klasy Point)
        """

        total_balls = self.config['regular_balls_number'] + \
            self.config['tracked_balls_number']
        columns_number = rows_number = math.ceil(math.sqrt(total_balls))

        area_width = int(self.scene_rectangle.width / columns_number)
        area_height = int(self.scene_rectangle.height / rows_number)
        busy_areas = [[False] * columns_number for y in range(rows_number)]

        positions = []
        for _ in range(total_balls):
            while True:
                x = random.randint(0, columns_number - 1)
                y = random.randint(0, rows_number - 1)
                if not busy_areas[y][x]:
                    busy_areas[y][x] = True
                    break

            rect = Rectangle(
                self.scene_rectangle.x + area_width *
                x + self.config['balls_radius'],
                self.scene_rectangle.y + area_height *
                y + self.config['balls_radius'],
                area_width - 2 * self.config['balls_radius'],
                area_height - 2 * self.config['balls_radius']
            )

            positions.append(rect.random_point())

        return positions
