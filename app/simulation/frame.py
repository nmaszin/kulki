import copy

from app.math.rectangle import Rectangle
from app.simulation.ball import Ball, TrackedBall


class SimulationFrame:
    def __init__(self, scene_rectangle, balls):
        self.scene_rectangle = scene_rectangle
        self.balls = balls

    def after(self, delta_time):
        """
        This method is responsible for generating the next frame
        that will occur after some delta_time
        """
        balls = copy.deepcopy(self.balls)

        for ballIndex, ball in enumerate(balls):
            for otherIndex, other in enumerate(balls[ballIndex + 1:]):
                if ball.is_collision_with_ball(other):
                    if not ball.has_ball_collided_at_last_frame(otherIndex):
                        ball.bounce_off_of_ball(other)
                        ball.register_ball_collided(otherIndex)
                elif ball.has_ball_collided_at_last_frame(otherIndex):
                    ball.unregister_ball_collided(otherIndex)


        for ball in balls:
            if ball.is_collision_with_wall(self.scene_rectangle):
                ball.bounce_off_of_wall(self.scene_rectangle)

        for ball in balls:
            ball.update(delta_time)

        return SimulationFrame(
            self.scene_rectangle,
            balls
        )

    def serialize(self):
        return {
            'scene': self.scene_rectangle.serialize(),
            'balls': [ball.serialize() for ball in self.balls]
        }

    @staticmethod
    def deserialize(data):
        deserialized_balls = []
        for ball in data['balls']:
            if ball['type'] == 'regular_ball':
                deserialized_balls.append(Ball.deserialize(ball))
            else:
                deserialized_balls.append(TrackedBall.deserialize(ball))

        return SimulationFrame(
            Rectangle.deserialize(data['scene']),
            deserialized_balls
        )
