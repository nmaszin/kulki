import math
import random

from app.math.vector import Vector


class Point:
    """
    Klasa definiująca pojęcie punktu oraz operacje,
    jakie można na nim wykonać
    """

    def __init__(self, x, y):
        """
        Konstruktor klasy. Jako parametry są przekazywane współrzędne punktu
        """

        self.x = x
        self.y = y

    def distance(self, other):
        """
        Metoda licząca dystans pomiędzy obecnym punktem, a jakimś innym
        """

        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def translate(self, vector):
        """
        Metoda, która dokonuje translacji punktu o wektor
        (wektor przyczepiamy do puntu, a grot wektora wyznacza nowe współrzędne)
        """

        return Point(
            self.x + vector.x,
            self.y + vector.y
        )

    def __str__(self):
        """
        Metoda, która opisuje w jaki sposób ma zostać dokonana konwersja na napis
        """
        return f'({self.x}, {self.y})'

    def __iter__(self):
        """
        Metoda, która określa, w jaki sposób będziemy iterować po obiekcie.
        Jest to potrzebne na przykład do konwersji punktu z klasy Point na tuple
        """

        yield self.x
        yield self.y

    def serialize(self):
        """
        Metoda która serializuje obiekt
        (konwertuje go do postaci, która jest bardziej przenośna; można ją np. zapisać do pliku)
        """

        return {
            'x': self.x,
            'y': self.y
        }

    @staticmethod
    def deserialize(data):
        """
        Metoda statyczna, która deserializuje obiekt (tworzy nowy obiekt,
        na podstawie zserializowanych danych)
        """

        return Point(
            data['x'],
            data['y']
        )
