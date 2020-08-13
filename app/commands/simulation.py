import yaml
import json
import climmands
from datetime import datetime

from app.simulation.simulation import Simulation
from app.visualisation.window import VisualisationWindow
from app.simulation.file import SimulationFile
from app.config import SimulationConfig
from app.simulation.generator import FrameGenerator
from app.simulation.results import ResultsObtainer
from app.config import ConfigObtainer

from app.math.vector import Vector

class SimulationCommand(climmands.Command):
    name = 'simulation'
    description = 'Run a simulation'

    def initialize_arguments_parser(self, parser):
        parser.add_argument('--config', help='Path to config file')
        parser.add_argument('--visual', action='store_true', help='Render simulation\'s visualisation')
        parser.add_argument('--json', action='store_true', help='Print results as json')

        subparsers = parser.add_subparsers(dest='action')
        
        save_parser = subparsers.add_parser('save', help='Save simulation to file')
        save_parser.add_argument('file', nargs='?', help='Simulation file')

        load_parser = subparsers.add_parser('load', help='Load demo from file')
        load_parser.add_argument('file', help='Simulation file')

    def execute(self, parsed_arguments):
        simulation = self.obtain_simulation(parsed_arguments)    
        self.save_simulation_if_specified(parsed_arguments, simulation)
        last_frame = self.perform_simulation(simulation, parsed_arguments.visual)
        self.print_statistics(parsed_arguments.json, last_frame)


    def obtain_simulation(self, parsed_arguments):
        if parsed_arguments.action == 'load':
            return SimulationFile(parsed_arguments.file).read()
    
        config = ConfigObtainer(parsed_arguments.config).obtain()
        initial_frame = FrameGenerator(config).generate()
        return Simulation(config, initial_frame)

    def save_simulation_if_specified(self, parsed_arguments, simulation):
        if parsed_arguments.action == 'save':
            SimulationFile(parsed_arguments.file).write(simulation)

    def perform_simulation(self, simulation, with_visualisation):
        if with_visualisation:
            return VisualisationWindow(simulation).run()
        else:
            return self.nonvisual_simulation(simulation)

    def nonvisual_simulation(self, simulation):  
        try:
            while not simulation.should_end():
                simulation.generate_next_frame()
                simulation.go_to_next_frame()
        except KeyboardInterrupt:
            pass

        return simulation.current_frame()

    def print_statistics(self, as_json, last_frame):
        results = ResultsObtainer(last_frame).obtain()

        if as_json:
            print(json.dumps(results, indent=4, sort_keys=True))
        else:
            for index, ball in enumerate(results):
                print(f'Tracked ball nr {index + 1}')
                for key, value in ball.items():
                    print(f'\t{key} = {value}')

                print()
