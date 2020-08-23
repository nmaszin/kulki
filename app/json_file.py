import json


class JsonFileException(Exception):
    """
    Wyjątek klasy JsonFile
    Jest rzucany w razie wszelkich niepowodzeń odczytu/zapisu
    do pliku JSON
    """


class JsonFile:
    """
    Klasa, która stanowi pewną wygodną abstrakcję na plik JSON.
    """

    def __init__(self, path):
        """
        Konstruktor klasy, przekazujemy do niego jako parametr ścieżkę do pliku
        """

        self.path = path

    def read(self):
        """
        Metoda odczytuje i parsuje dane z pliku JSON, wskazanego w konstruktorze
        """

        try:
            with open(self.path, 'r') as f:
                return json.load(f)
        except IOError:
            raise JsonFileException(f'Error reading file {self.path}')

    def write(self, data):
        """
        Metoda zapisuje dane do pliku JSON, wskazanego w konstruktorze
        """

        try:
            with open(self.path, 'w') as f:
                json.dump(data, f, indent=4)
        except IOError:
            raise JsonFileException(f'Error writing file {self.path}')
