import math
import random

class Vector:
    """
    Klasa implementująca wektor
    """

    def __init__(self, x, y):
        """
        Konstruktor klasy. Jako parametry przekazywane są współrzędne wektora
        """

        self.x = x
        self.y = y

    @staticmethod
    def from_polar(r, phi):
        """
        Metoda statyczna, który tworzy wektor w analogiczny sposób,
        mianowicie z postaci biegunowej
        """

        return Vector(
            r * math.cos(phi),
            r * math.sin(phi)
        )

    def __str__(self):
        """
        Metoda, która opisuje w jaki sposób ma zostać dokonana konwersja na napis
        """

        return f'[{self.x}, {self.y}]'

    def __add__(self, other):
        """
        Metoda, która obsługuje operację dodawania dwóch wektorów, i zwraca wektor wynikowy.
        Jest wywoływana niejawnie, w momencie stosowania operatora +, np.: v1 + v2
        """

        return Vector(
            self.x + other.x,
            self.y + other.y
        )

    def __sub__(self, other):
        """
        Metoda, która obsługuje operację odejmowania dwóch wektorów, i zwraca wektor wynikowy.
        Jest wywoływana niejawnie, w momencie stosowania operatora -, np.: v1 - v2
        """

        return Vector(
            self.x - other.x,
            self.y - other.y
        )

    def __mul__(self, scale):
        """
        Metoda, która obsługuje operację skalowania wektora (mnożenia wektora przez skalar)
        i zwraca wektor wynikowy.
        Jest wywoływana niejawnie, w momencie stosowania operatora *, np.: v * 997
        """

        return Vector(
            self.x * scale,
            self.y * scale
        )

    def __abs__(self):
        """
        Metoda zwraca moduł wektora (długość)
        """

        return math.sqrt(self.x ** 2 + self.y ** 2)

    def dot(self, other):
        """
        Metoda liczy iloczyn skalarny dwóch wektorów
        """

        return self.x * other.x + self.y * other.y

    def angle(self, other):
        """
        Metoda liczy kąt pomiędzy dwoma wektorami i wyraża go w stopniach
        """

        return math.degrees(
            math.acos(self.dot(other) / (abs(self) * abs(other)))
        )

    def ortogonal(self):
        """
        Metoda zwraca pewien wektor, który jest prostopadły do obecnego
        (zwrot i długość wektora są nieznane)
        """

        x = 1
        if self.y != 0:
            return Vector(
                x,
                -x * self.x / self.y
            )
        else:
            return Vector(
                self.y,
                self.x
            )

    def norm(self):
        """
        Metoda zwraca wektor unormowany (obecny wektor jest skracany, bądź
        wydłużany, tak aby osiągnął długość 1)
        """

        scale = 1 / abs(self)
        return self * scale

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

        return Vector(
            data['x'],
            data['y']
        )

    @staticmethod
    def generate(data):
        """
        Metoda statyczna, która generuje losowy wektor, na podstawie parametrów
        które zostały przekazane w zmiennej data
        """

        min_angle, max_angle = data['angle']
        min_value, max_value = data['value']

        angle = random.randint(min_angle, max_angle)
        value = random.randint(min_value, max_value)

        return Vector.from_polar(value, angle)
