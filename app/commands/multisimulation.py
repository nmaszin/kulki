import sys
import copy
import json
import climmands
from datetime import datetime

from app.json_file import JsonFile
from app.config import ConfigObtainer
from app.simulation.simulation import Simulation
from app.simulation.results import ResultsObtainer
from app.simulation.generator import FrameGenerator


class MultiSimulationCommand(climmands.Command):
    """
    Klasa kontrolera komendy multisimulation
    """

    name = 'multisimulation'
    description = 'Perform multiple simulations for different balls number'

    def initialize_arguments_parser(self, parser):
        """
        Metoda, która wskazuje, jakie parametry wywołania można przekazać do komendy
        Parametry te zostają ustawione w parserze, który jest przekazywany jako jedyny argument
        """

        parser.add_argument('results', help='Path to file with results')
        parser.add_argument('--config', help='Path to config file')

    def execute(self, parsed_arguments):
        """
        Metoda, która obsługuje to, w jaki sposób wykonuje się komenda
        W parametrze parsed_arguments znajdują się wszystkie argumenty wywołania
        przekazane od użytkownika
        """

        config = ConfigObtainer(parsed_arguments.config).obtain()
        if 'simulation_max_frames' not in config:
            print('simulation_max_frames property not specified')
            return

        results = {}

        initial, step, number = config['multisimulation_balls_number_sequence']
        for index in range(number):
            current_balls_number = initial + index * step
            config['regular_balls_number'] = current_balls_number
            print(f"Running simulation for: M = {config['simulation_max_frames']}, N = {current_balls_number}", file=sys.stderr)

            initial_frame = FrameGenerator(config).generate()
            last_frame = self.__nonvisual_simulation(config, initial_frame)
            current_results = ResultsObtainer(last_frame).obtain()

            results[current_balls_number] = current_results

        JsonFile(parsed_arguments.results).write(results)


    def __nonvisual_simulation(self, config, initial_frame):
        """
        Metoda, która odpowiada za przeprowadzenie symulacji bez wizualizacji
        """

        simulation = Simulation(config, initial_frame)
        while not simulation.should_end():
            simulation.generate_next_frame()
            simulation.go_to_next_frame()

        return simulation.current_frame()
