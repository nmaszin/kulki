import pygame
from pygame import gfxdraw


class Circle:
    """
    Klasa jest wrapperem (nakładką), który pozwala w prosty sposób
    rysować koło z anty-aliasingiem (wygładzaniem krawędzi)
    """

    def __init__(self, point, radius, color):
        """
        Konstruktor klasy. Przekazywane mu są następujące argumenty:
            - point - obiekt klasy Point; punkt, określający pozycję środka okręgu
            - radius - wartość skalarna, określająca promień okręgu
            - color - trzyelementowa krotka określająca kolor (patrz w klasę Color)
        """

        self.point = point
        self.radius = radius
        self.color = color

    def draw(self, surface):
        """
        Metoda rysująca koło z antyaliasingiem.
        Rysowanie odbywa się na powierzchni,
        która została przekazana jako jedyny argument.
        """

        params = (
            surface,
            *tuple(map(int, self.point)),
            self.radius,
            self.color
        )

        gfxdraw.aacircle(*params)
        gfxdraw.filled_circle(*params)
