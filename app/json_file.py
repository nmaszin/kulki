import json


class JsonFileException(Exception):
    pass


class JsonFile:
    def __init__(self, path):
        self.path = path

    def read(self):
        try:
            with open(self.path, 'r') as f:
                return json.load(f)
        except IOError:
            raise JsonFileException(f'Error reading file {self.path}')

    def write(self, data):
        try:
            with open(self.path, 'w') as f:
                json.dump(data, f, indent=4)
        except IOError:
            raise JsonFileException(f'Error writing file {self.path}')
