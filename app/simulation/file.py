import json
from datetime import datetime

from app.json_file import JsonFile
from app.simulation.simulation import Simulation


class SimulationFile:
    """
    Klasa obsługująca zapis symulacji do pliku JSON i odczyt z niego
    """

    def __init__(self, path):
        """
        Konstruktor klasy. Jako argument przekazywana jest ścieżka do pliku z symulacją
        """

        self.path = path

    def read(self):
        """
        Metoda wczytuje symulację z pliku JSON i zwraca obiekt klasy Simulation
        """

        return Simulation.deserialize(JsonFile(self.path).read())

    def write(self, simulation):
        """
        Metoda zapisuje obiekt klasy Simulation do pliku JSON
        """

        JsonFile(self.path).write(simulation.serialize())

    @staticmethod
    def generate_name():
        """
        Metoda statyczna generuje nazwę pliku z symulacją,
        co jest stosowane jeżeli użytkownik poprosi o zapis symulacji,
        a nie poda jej nazwy.

        Nazwa zawiera datę i czas wygenerowania nazwy oraz rozszerzenie 'sim'.
        """

        time_string = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        extension = 'sim'
        return f'{time_string}.{extension}'
