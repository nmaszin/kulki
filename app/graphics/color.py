import random


class Color:
    """
    Klasa służąca do zarządzania kolorami w programie
    Po pierwsze, przechowuje pewne szczególne kolory:
        - kolor tła
        - kolor zwykłej kulki
        - kolor kulki śledzonej

    Po drugie, pozwala losować kolory
    Po trzecie, pozwala mieszać kolory

    Co istotne, kolory nie są obiektami tej klasy,
    ale trzy-elementowymi krotkami (tuple).
    Natomiast klasa ta dokonuje na nich operacji,
    poprzez metody statyczne
    """

    BACKGROUND = (20, 20, 20)
    BALL = (240, 0, 0)
    TRACKED_BALL = (100, 100, 240)
    BOUNCED_BALL = (100, 240, 100)
    TRACK = (14, 163, 54)

    @staticmethod
    def mix(weight, first_color, second_color):
        """
        Metoda miesza dwa kolory, na podstawie wagi (która dotyczy tego pierwszego koloru)
        """
        return tuple(map(lambda x: int(x[0] * weight + x[1] * (1 - weight)), zip(first_color, second_color)))

    @staticmethod
    def random():
        """
        Metoda losuje pewien kolor
        """
        r = random.randint(20, 240)
        g = random.randint(20, 240)
        b = random.randint(20, 240)
        return (r, g, b)
