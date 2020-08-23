from app.math.vector import Vector


class TransformationMatrix:
    """
    Klasa implementuje macierz przejścia z bazy do bazy (2x2)
    Macierz ta jest potrzebna, aby móc w prosty sposób
    przekształcać jakiś wektor z jednego układu współrzędnych
    do innego
    """

    def __init__(self, unit_vector_x, unit_vector_y):
        """
        Konstruktor klasy. Jako argumenty, przekazywane mu są wektory jednostkowe,
        które opisują nowy układ współrzędnych
        """

        self.a, self.b = unit_vector_x.x, unit_vector_x.y
        self.c, self.d = unit_vector_y.x, unit_vector_y.y

    def __mul__(self, scale):
        """
        Metoda specjalna, która implementuje operację mnożenia macierzy przez skalar.
        Metoda ta wywoływana jest niejawnie, kiedy korzystamy z operatora "*" w taki sposób:
            matrix * scale
        """

        return TransformationMatrix(
            Vector(self.a, self.b) * scale,
            Vector(self.c, self.d) * scale
        )

    def inverse(self):
        """
        Metoda, która liczy macierz odwrotną, do obecnej,
        a następnie zwraca ową macierz odwrotną
        """

        a, b, c, d = self.a, self.b, self.c, self.d
        scale = 1 / (a * d - b * c)
        matrix = TransformationMatrix(
            Vector(d, -b),
            Vector(-c, a)
        )

        return matrix * scale

    def multiple_by_vector(self, vector):
        """
        Metoda, która implementuje mnożenie macierzy przez wektor
        """

        a, b, c, d = self.a, self.b, self.c, self.d
        return Vector(
            a * vector.x + c * vector.y,
            b * vector.x + d * vector.y
        )

    def to_base(self, vector):
        """
        Metoda, która przekształca wektor ze starej bazy, do nowej
        (opisywanej przez wektory, które zostały przekazane do konstruktora)
        """

        matrix = self.inverse()
        return matrix.multiple_by_vector(vector)

    def from_base(self, vector):
        """
        Metoda, która przekształca wektor z powrotem do starej bazy, z nowej
        (opisanej przez wektory, które zostały przekazane do konstruktora)
        """
        return self.multiple_by_vector(vector)
