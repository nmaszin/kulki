from app.simulation.ball import Ball, TrackedBall
from app.visualisation.ball import DrawableBall, DrawableTrackedBall
from app.color import Color


class DrawableFrame:
    def __init__(self, frame):
        self.frame = frame

    def draw(self, surface):
        for ball in self.frame.balls:
            if isinstance(ball, TrackedBall):
                DrawableTrackedBall(ball, Color.TRACKED_BALL,
                                    Color.TRACK, Color.BOUNCED_BALL).draw(surface)
            else:
                DrawableBall(ball, Color.BALL).draw(surface)
