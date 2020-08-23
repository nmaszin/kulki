import math
import random
import json
from multicon import Config

from app.math.vector import Vector
from app.json_file import JsonFile


class SimulationConfig(Config):
    """
    Klasa obsługująca konfigurację.
    Bazuje na klasie Config z biiblioteki multicon
    i wprowadza pewien zestaw opcji domyślnych
    """

    DEFAULTS = {
        'width': 600,
        'height': 600,
        'fullscreen': False,
        'fps': 60,
        'engine_fps': 60,
        'exit_at_the_end_of_simulation': True,

        'collisions_precision': 1,
        'balls_radius': 10,
        'track_dots_radius': 2,

        'regular_balls_number': 10,
        'regular_balls_velocity': {
            'angle': [0, 360],
            'value': [0, 500]
        },
        'regular_balls_acceleration': {
            'angle': [0, 0],
            'value': [0, 0]
        },

        'tracked_balls_number': 1,
        'tracked_balls_velocity': {
            'angle': [0, 360],
            'value': [0, 500]
        },
        'tracked_balls_acceleration': {
            'angle': [0, 0],
            'value': [0, 0]
        },
    }

    def __init__(self, config):
        """
        Konstruktor, inicjalizuje klasę bazową pewnym zestawem
        opcji domyślnych oraz konfiguracją użytkownika, przekazaną
        poprzez parametr config
        """

        super().__init__(self.DEFAULTS, config)

    def serialize(self):
        """
        Metoda która serializuje obiekt
        (konwertuje go do postaci, która jest bardziej przenośna; można ją np. zapisać do pliku)
        """

        return self.custom

    @staticmethod
    def deserialize(data):
        """
        Metoda statyczna, która deserializuje obiekt (tworzy nowy obiekt,
        na podstawie zserializowanych danych)
        """

        return SimulationConfig(data)


class ConfigObtainer:
    """
    Klasa pomocnicza, która pozwala w prosty sposób uzyskać
    konfigurację symulacji, niezależnie od tego, czy użytkownik
    użył opcjonalnego parametru --config podczas wywołania komendy, czy też nie
    """

    def __init__(self, path=None):
        """
        Konstruktor klasy. Jako parametr path przekazywana jest ścieżka
        do pliku z konfiguracją, przekazana przez użytkownika poprzez parametr --config.
        Jeżeli użytkownik takowej nie przekazał, path ma wartość None
        """

        self.path = path

    def obtain(self):
        """
        Jeżeli użytkownik nie podał ścieżki do pliku z konfiguracją, zakładamy że
        zestaw jego opcji konfiguracyjnych jest pusty. Jeżeli podał ścieżkę - zestaw ten odczytujemy
        z pliku. Na jego podstawie konstruujemy obiekt SimulationConfig, który zwracamy
        """

        if self.path is None:
            custom_config = {}
        else:
            custom_config = JsonFile(self.path).read()

        return SimulationConfig(custom_config)
