from collections import deque

from app.math.point import Point
from app.math.vector import Vector
from app.math.rectangle import Rectangle
from app.math.matrix import TransformationMatrix
from app.graphics.circle import Circle


class Ball:
    """
    Klasa realizująca matematyczny model kulki
    Obsługuje ruch, oraz zderzenia ze ścianami oraz innymi obiektami
    """

    def __init__(self, position, radius, velocity, acceleration, collisions_precision):
        """
        Konstruktor klasy. Przekazywane mu są następujące parametry:
            - position - obiekt klasy Point, punkt określający położenie środka kulki
            - radius - wartość skalarna, długość promienia kulki
            - velocity - obiekt klasy Vector, wektor prędkości chwilowej kulki
            - acceleration - obiekt klasy Vector, wektor przyspieszenia kulki
            - collisions_precision - wartość skalarna określająca precyzję kolizji
                (odległość pomiędzy krawędziami kulek, przy której następuje kolizja)
        """

        self.position = position
        self.radius = radius
        self.velocity = velocity
        self.acceleration = acceleration
        self.collisions_precision = collisions_precision

        # Lista wszystkich kulek, z jakimi w poprzedniej klatce zderzyła się obecna kulka
        # Ma to zastosowanie do obsługi błędów, jakie pojawiają się czasem podczas kolizji
        self.balls_collided_at_last_frame = []

    def is_collision_with_ball(self, ball):
        """
        Metoda zwraca True, jeżeli obecna kulka jest w stanie kolizji z kulką, przekazaną
        jako argument
        """

        distance = self.position.distance(ball.position)
        return distance <= self.radius + ball.radius + self.collisions_precision

    def is_collision_with_wall(self, scene_rectangle):
        """
        Metoda zwraca True, jeżeli obecna kulka jest w stanie kolizji z którąś ze ścian
        """

        return not self.ball_possible_centers(scene_rectangle).contains(self.position)

    def register_ball_collided(self, ballIndex):
        """
        Metoda rejestruje, że w poprzedniej klatce wystąpiła kolizja
        Ma to zastosowanie do obsługi błędów, jakie pojawiają się czasem podczas kolizji
        """
        self.balls_collided_at_last_frame.append(ballIndex)

    def unregister_ball_collided(self, ballIndex):
        """
        Metoda odnotowuje, że w poprzedniej klatce obecna kulka, nie zderzyła się z inną,
        przekazaną jako parametr.
        Ma to zastosowanie do obsługi błędów, jakie pojawiają się czasem podczas kolizji
        """

        self.balls_collided_at_last_frame.remove(ballIndex)

    def has_ball_collided_at_last_frame(self, ballIndex):
        """
        Metoda zwraca True, jeżeli w poprzedniej klatce obecna kulka uległa kolizji z inną,
        przekazaną jako parametr.
        Ma to zastosowanie do obsługi błędów, jakie pojawiają się czasem podczas kolizji
        """
        return ballIndex in self.balls_collided_at_last_frame

    def bounce_off_of_ball(self, ball):
        """
        Metoda obsługuje zderzenie się dwóch kulek.
        Zmianie ulegają jedynie wektory ich prędkości
        """

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
        Metoda obsługuje odbijanie się kulki od ścian.
        Zmianie ulega jedynie wektor prędkości kulki.

        Kolizje są dodatkowo zabezpieczone, aby kulka nie utknęła w ścianie
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
        Metoda zwraca prostokąt (obiekt klasy Rectangle)
        który zawiera wszystkie możliwe punkty, jakie może przyjąć środek kulki,
        poruszającej się swobodnie po naczyniu (czyli scenie).

        Mówiąc inaczej, jeżeli środek kulki nie należy do tego obszaru,
        znajduje się w stanie kolizji z którąś ze ścian
        """

        return Rectangle(
            x=scene_rectangle.x + self.radius + self.collisions_precision,
            y=scene_rectangle.y + self.radius + self.collisions_precision,
            width=scene_rectangle.width - 2 * self.radius - 2 * self.collisions_precision,
            height=scene_rectangle.height - 2 * self.radius - 2 * self.collisions_precision,
        )

    def update(self, time_delta):
        """
        Metoda aktualizuje wektor prędkości oraz położenie kulki
        po czasie time_delta.
        Zakładamy, że ruch jest chwilowo jednostajny.

        Metoda zwraca drogę, jaką kulka przebyła między dwoma klatkami,
        czyli odległość pomiędzy pozycją kulki przed wywołaniem metody update(),
        a pozycją po wywołaniu tejże metody.
        """

        velocity_displacement = self.acceleration * time_delta
        self.velocity += velocity_displacement

        displacement = self.velocity * time_delta
        self.position = self.position.translate(displacement)

        return abs(displacement)

    def serialize(self):
        """
        Metoda która serializuje obiekt
        (konwertuje go do postaci, która jest bardziej przenośna; można ją np. zapisać do pliku)
        """

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
        """
        Metoda statyczna, która deserializuje obiekt (tworzy nowy obiekt,
        na podstawie zserializowanych danych)
        """

        return Ball(
            Point.deserialize(data['position']),
            data['radius'],
            Vector.deserialize(data['velocity']),
            Vector.deserialize(data['acceleration']),
            data['collisions_precision']
        )


class TrackedBall(Ball):
    """
    Klasa realizująca matematyczny model kulki śledzonej.
    Klasa ta dziedziczy po klasie zwykłej kulki, a więc obowiązuje
    ją ta sama fizyka.

    Klasa ta dodatkowo zbiera informacje o poprzednich pozycjach kulki,
    ilości kolizji oraz ścieżkch swobodnych.
    """

    TRACK_SIZE = 100

    def __init__(self, position, radius, velocity, acceleration, collisions_precision):
        """
        Konstruktor klasy. Przekazywane parametry są identyczne, jak w klasie Ball.

        Najpierw wywoływany jest konstruktor klasy bazowej Ball, a następnie
        inicjalizowane są pola szczególne dla klasy TrackedBall
        """

        super().__init__(position, radius, velocity, acceleration, collisions_precision)
        self.previous_positions = deque([])

        self.collision_effect = 0  # Używane jako waga koloru podczas wizualizacji odbić
        self.collisions_counter = 0

        self.free_paths = []
        self.current_free_path = 0

    def update(self, time_delta):
        """
        Metoda przesłania metodę update() z klasy bazowej,
        aby rozserzyć ją o zbieranie informacji o poprzednich pozycjach
        oraz ścieżce swobodnej
        """

        self.collision_effect = max(self.collision_effect - 0.04, 0)

        self.previous_positions.append(self.position)
        if len(self.previous_positions) > self.TRACK_SIZE:
            self.previous_positions.popleft()

        displacement = super().update(time_delta)
        self.current_free_path += displacement
        return displacement

    def bounce_off_of_ball(self, ball):
        """
        Metoda przesłania analogiczną metodę z klasy bazowej,
        rozszerzając ją m.in. o zbieranie informacji na temat ilości kolizji
        """

        super().bounce_off_of_ball(ball)

        self.collision_effect = 1
        self.collisions_counter += 1

        self.free_paths.append(self.current_free_path)
        self.current_free_path = 0

    def statistics(self):
        """
        Metoda zwraca statystyki zgromadzone przez obecną kulkę:
            - liczbę kolizji od początku symulacji
            - średnią ścieżkę swobodną
        """

        def avg(x):
            """
            Funkcja liczy średnią arytmetyczną elementów zawartych w liście x
            W przypadku, gdyby była ona pusta, zwrócone zostanie None
            """

            try:
                return sum(x) / len(x)
            except ZeroDivisionError:
                pass

        return {
            'collisions_counter': self.collisions_counter,
            'average_free_path': avg(self.free_paths)
        }

    def serialize(self):
        """
        Metoda która serializuje obiekt
        (konwertuje go do postaci, która jest bardziej przenośna; można ją np. zapisać do pliku)
        """

        return {
            **super().serialize(),
            **{'type': 'tracked_ball'}
        }

    @staticmethod
    def deserialize(data):
        """
        Metoda statyczna, która deserializuje obiekt (tworzy nowy obiekt,
        na podstawie zserializowanych danych)
        """

        return TrackedBall(
            Point.deserialize(data['position']),
            data['radius'],
            Vector.deserialize(data['velocity']),
            Vector.deserialize(data['acceleration']),
            data['collisions_precision']
        )
