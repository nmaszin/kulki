from app.graphics.color import Color
from app.graphics.circle import Circle

class DrawableBall:
    """
    Klasa, która odpowiada za rysowanie modelu klasy Ball na oknie wizualizacji
    """

    def __init__(self, ball, color):
        """
        Konstruktor, przekazujemy mu obiekt klasy Ball oraz kolor, jaki ma mieć kulka
        """

        self.ball = ball
        self.color = color

    def draw(self, surface):
        """
        Metoda, która rysuje kulkę na powierzchni 'surface'
        """

        Circle(self.ball.position, self.ball.radius, self.color).draw(surface)


class DrawableTrackedBall(DrawableBall):
    """
    Klasa, która odpowiada za rysowanie kulki śledzonej na oknie wizualizacji
    """

    def __init__(self, ball, track_dot_radius, color, track_color, bounce_color):
        """
        Konstruktor klasy. Jako parametry przyjmuje kulkę śledzoną, rozmiar rysowanego śladu
        oraz kolory: kulki, śladu oraz kulki po odbiciu
        """

        mixed_color = Color.mix(
            ball.collision_effect,
            bounce_color,
            color
        )

        super().__init__(ball, mixed_color)
        self.track_color = track_color
        self.track_dot_radius = track_dot_radius

    def draw(self, surface):
        """
        Metoda, która rysuje kulkę i jej ślad na powierzchni 'surface'
        """

        for index, position in enumerate(self.ball.previous_positions):
            weight = index / len(self.ball.previous_positions)
            color = Color.mix(weight, self.track_color, Color.BACKGROUND)

            Circle(position, self.track_dot_radius,
                   color).draw(surface)

        super().draw(surface)
