import json
from datetime import datetime

from app.simulation.simulation import Simulation
from app.json_file import JsonFile

class SimulationFile:
    def __init__(self, path):
        self.path = path

    def read(self):
        return Simulation.deserialize(JsonFile(self.path).read())
            
    def write(self, simulation):
        JsonFile(self.path).write(simulation.serialize())

    @staticmethod
    def generate_name():
        time_string = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        extension = 'sim'
        return f'{time_string}.{extension}'