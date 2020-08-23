import random

from app.math.point import Point


class Rectangle:
    """
    Klasa implementująca prostokąt
    """

    def __init__(self, x, y, width, height):
        """
        Konstruktor klasy. Przekazywane mu są następujące parametry:
            - x, y - współrzędne lewego-górnego wierzchołka prostokąta
            - width, height - odpowiednio szerokość i wysokość prostokąta
        """

        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def random_point(self):
        """
        Metoda losuje dowolny punkt, spośród tych, które należą do prostokąta
        """

        return Point(
            random.randint(self.x, self.x + self.width),
            random.randint(self.y, self.y + self.height),
        )

    def contains(self, point):
        """
        Metoda zwraca True, jeżeli punkt należy do prostokąta
        """
        return self.left() <= point.x <= self.right() \
            and self.top() <= point.y <= self.bottom()

    def left(self):
        """
        Metoda zwraca współrzędną lewego boku prostokąta
        """

        return self.x

    def top(self):
        """
        Metoda zwraca współrzędną górnego boku prostokąta
        """

        return self.y

    def right(self):
        """
        Metoda zwraca współrzędną prawego boku prostokąta
        """

        return self.x + self.width

    def bottom(self):
        """
        Metoda zwraca współrzędną dolnego boku prostokąta
        """

        return self.y + self.height

    def serialize(self):
        """
        Metoda która serializuje obiekt
        (konwertuje go do postaci, która jest bardziej przenośna; można ją np. zapisać do pliku)
        """

        return {
            'x': self.x,
            'y': self.y,
            'width': self.width,
            'height': self.height
        }

    @staticmethod
    def deserialize(data):
        """
        Metoda statyczna, która deserializuje obiekt (tworzy nowy obiekt,
        na podstawie zserializowanych danych)
        """

        return Rectangle(
            data['x'],
            data['y'],
            data['width'],
            data['height']
        )
