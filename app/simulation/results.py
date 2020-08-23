from app.simulation.ball import TrackedBall


def as_list(generator):
    return lambda *args, **kwargs: list(generator(*args, **kwargs))


class ResultsObtainer:
    """
    Klasa, która uzyskuje statystyki wszystkich kulek śledzonych
    z danej klatki
    """

    def __init__(self, frame):
        """
        Konstruktor klasy. Jako argument przekazywana jest klatka,
        z której mają zostać uzyskane stosowne informacje
        """

        self.frame = frame

    @as_list
    def obtain(self):
        """
        Metoda, która generuje informacje o każdej kulce śledzonej.
        Są one później zwracane w postaci listy.
        """

        for ball in self.frame.balls:
            if isinstance(ball, TrackedBall):
                yield ball.statistics()
