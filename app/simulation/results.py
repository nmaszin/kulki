from app.simulation.ball import TrackedBall


def as_list(generator):
    return lambda *args, **kwargs: list(generator(*args, **kwargs))


class ResultsObtainer:
    def __init__(self, frame):
        self.frame = frame

    @as_list
    def obtain(self):
        for ball in self.frame.balls:
            if isinstance(ball, TrackedBall):
                yield ball.statistics()
