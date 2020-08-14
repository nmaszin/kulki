from collections import deque

from app.math.point import Point
from app.math.vector import Vector
from app.math.rectangle import Rectangle
from app.math.matrix import TransformationMatrix
from app.graphics.circle import Circle


class Ball:
    """
    Mathematical model of ball
    This class handle move and collisions with wall and other objects
    """

    def __init__(self, position, radius, velocity, acceleration, collisions_precision):
        self.position = position
        self.radius = radius
        self.velocity = velocity
        self.acceleration = acceleration
        self.collisions_precision = collisions_precision

        self.balls_collided_at_last_frame = []

    def __eq__(self, other):
        return self.position == other.position and self.velocity == other.velocity and self.radius == other.radius

    def is_collision_with_ball(self, ball):
        """
        Returns True if collision between two balls has ocurred
        """
        distance = self.position.distance(ball.position)
        collision_detected = distance <= self.radius + ball.radius + self.collisions_precision
        can_handle_collision = ball not in self.balls_collided_at_last_frame
        return collision_detected and can_handle_collision

    def is_collision_with_wall(self, scene_rectangle):
        """
        Returns True if collision between ball and wall has ocurred
        Wall is a border of scene rectangle
        """
        return not self.ball_possible_centers(scene_rectangle).contains(self.position)

    def bounce_off_of_ball(self, ball):
        """
        Handle ball bouncing off of another ball
        Does not return anything
        """
        self.balls_collided_at_last_frame.append(ball)

        vector_between_centers = Vector(
            ball.position.x - self.position.x,
            ball.position.y - self.position.y
        )

        vector_x = vector_between_centers.norm()
        vector_y = vector_between_centers.ortogonal().norm()
        matrix = TransformationMatrix(vector_x, vector_y)

        self_velocity_transformed = matrix.to_base(self.velocity)
        ball_velocity_transformed = matrix.to_base(ball.velocity)

        # First coordinates exchange
        # Second coordinate is preserved
        temp = self_velocity_transformed.x
        self_velocity_transformed.x = ball_velocity_transformed.x
        ball_velocity_transformed.x = temp

        self.velocity = matrix.from_base(self_velocity_transformed)
        ball.velocity = matrix.from_base(ball_velocity_transformed)

    def bounce_off_of_wall(self, scene_rectangle):
        """
        Handle ball bouncing off of walls
        Does not return anything
        """
        possible_centers = self.ball_possible_centers(scene_rectangle)

        if self.position.x < possible_centers.left() and self.velocity.x < 0:
            self.velocity.x *= -1
        elif self.position.x > possible_centers.right() and self.velocity.x > 0:
            self.velocity.x *= -1

        if self.position.y < possible_centers.top() and self.velocity.y < 0:
            self.velocity.y *= -1
        elif self.position.y > possible_centers.bottom() and self.velocity.y > 0:
            self.velocity.y *= -1

    def ball_possible_centers(self, scene_rectangle):
        """
        Returns a rectangle that describes area
        consisting of all possible points (centers of ball)
        which ball is able to have
        """
        return Rectangle(
            x=scene_rectangle.x + self.radius + self.collisions_precision,
            y=scene_rectangle.y + self.radius + self.collisions_precision,
            width=scene_rectangle.width - 2 * self.radius - 2 * self.collisions_precision,
            height=scene_rectangle.height - 2 * self.radius - 2 * self.collisions_precision,
        )

    def update(self, time_delta):
        """
        Updates position of the ball after time_delta seconds
        Does not return anything
        """
        velocity_displacement = self.acceleration * time_delta
        self.velocity += velocity_displacement

        displacement = self.velocity * time_delta
        self.position = self.position.translate(displacement)

        self.balls_collided_at_last_frame = []

        return abs(displacement)

    def serialize(self):
        return {
            'type': 'regular_ball',
            'position': self.position.serialize(),
            'radius': self.radius,
            'velocity': self.velocity.serialize(),
            'acceleration': self.acceleration.serialize(),
            'collisions_precision': self.collisions_precision
        }

    @staticmethod
    def deserialize(data):
        return Ball(
            Point.deserialize(data['position']),
            data['radius'],
            Vector.deserialize(data['velocity']),
            Vector.deserialize(data['acceleration']),
            data['collisions_precision']
        )


class TrackedBall(Ball):
    TRACK_SIZE = 100

    def __init__(self, position, radius, velocity, acceleration, collisions_precision):
        super().__init__(position, radius, velocity, acceleration, collisions_precision)
        self.previous_positions = deque([])

        self.collision_effect = 0  # Used as color weight in visualisation
        self.collisions_counter = 0

        self.free_paths = []
        self.current_free_path = 0

    def update(self, time_delta):
        self.collision_effect = max(self.collision_effect - 0.04, 0)

        self.previous_positions.append(self.position)
        if len(self.previous_positions) > self.TRACK_SIZE:
            self.previous_positions.popleft()

        displacement = super().update(time_delta)
        self.current_free_path += displacement
        return displacement

    def bounce_off_of_ball(self, ball):
        super().bounce_off_of_ball(ball)

        self.collision_effect = 1
        self.collisions_counter += 1

        self.free_paths.append(self.current_free_path)
        self.current_free_path = 0

    def statistics(self):
        def avg(x): return sum(x) / len(x)
        return {
            'collisions_counter': self.collisions_counter,
            'average_free_path': avg(self.free_paths)
        }

    def serialize(self):
        return {
            **super().serialize(),
            **{'type': 'tracked_ball'}
        }

    @staticmethod
    def deserialize(data):
        return TrackedBall(
            Point.deserialize(data['position']),
            data['radius'],
            Vector.deserialize(data['velocity']),
            Vector.deserialize(data['acceleration']),
            data['collisions_precision']
        )
