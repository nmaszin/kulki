from app.color import Color
from app.graphics.circle import Circle


class DrawableBall:
    def __init__(self, ball, color):
        self.ball = ball
        self.color = color

    def draw(self, surface):
        Circle(self.ball.position, self.ball.radius, self.color).draw(surface)


class DrawableTrackedBall(DrawableBall):
    def __init__(self, ball, color, track_color, bounce_color):
        mixed_color = Color.mix(
            ball.collision_effect,
            bounce_color,
            color
        )

        super().__init__(ball, mixed_color)
        self.track_color = track_color

    def draw(self, surface):
        for position in self.ball.previous_positions:
            Circle(position, 2, self.track_color).draw(surface)

        super().draw(surface)
