from app.simulation.ball import Ball, TrackedBall
from app.visualisation.ball import DrawableBall, DrawableTrackedBall
from app.graphics.color import Color


class DrawableFrame:
    """
    Klasa, która odpowiada za rysowanie całej klatki symulacji (klasa SimulationFrame)
    na oknie wizualizacji
    """

    def __init__(self, frame, config):
        """
        Konstruktor klasy. Jako argumenty przekazujemy klatkę oraz konfigurację
        """

        self.frame = frame
        self.config = config

    def draw(self, surface):
        """
        Metoda, która rysuje klatkę na powierzchni 'surface'
        """

        for ball in self.frame.balls:
            if isinstance(ball, TrackedBall):
                DrawableTrackedBall(ball, self.config['track_dots_radius'], Color.TRACKED_BALL,
                                    Color.TRACK, Color.BOUNCED_BALL).draw(surface)
            else:
                DrawableBall(ball, Color.BALL).draw(surface)
