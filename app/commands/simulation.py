import yaml
import climmands
from datetime import datetime

from app.simulation.simulation import Simulation
from app.visualisation.window import VisualisationWindow
from app.simulation.file import FrameFile
from app.config import SimulationConfig
from app.simulation.generator import FrameGenerator
from app.simulation.results import ResultsObtainer
from app.config import YamlConfigFile, SimulationConfig

from app.math.vector import Vector

class SimulationCommand(climmands.Command):
    name = 'simulation'
    description = 'Run a simulation'

    def initialize_arguments_parser(self, parser):
        parser.add_argument('--config', help='Path to config file')
        parser.add_argument('--visualisation', action='store_true', help='Render simulation\'s visualisation')
        subparsers = parser.add_subparsers(dest='action')

        save_parser = subparsers.add_parser('save', help='Save simulation to file')
        save_parser.add_argument('file', nargs='?', help='Simulation file')

        load_parser = subparsers.add_parser('load', help='Load demo from file')
        load_parser.add_argument('file', help='Simulation file')

    def execute(self, parsed_arguments):
        config = self.obtain_config(parsed_arguments)
        initial_frame = self.obtain_initial_frame(config, parsed_arguments)
        last_frame = self.obtain_last_frame(config, initial_frame, parsed_arguments.visualisation)

        print(ResultsObtainer(last_frame).obtain())

    def obtain_initial_frame(self, config, parsed_arguments):
        if parsed_arguments.action == 'load':
            frame = FrameFile(parsed_arguments.file).read()
        elif parsed_arguments.action == 'save':
            frame = FrameGenerator(config).generate()
            filename = parsed_arguments.file or FrameGenerator.generate_name()
            FrameFile(filename).write(frame)
        else:
            frame = FrameGenerator(config).generate()

        return frame

    def obtain_config(self, parsed_arguments):
        config_path = parsed_arguments.config

        if config_path is None:
            custom_user_config = {}
        else:
            custom_user_config = YamlConfigFile(config_path).read()

        return SimulationConfig(custom_user_config)

    def obtain_last_frame(self, config, initial_frame, with_visualisation):
        if with_visualisation:
            return VisualisationWindow(config, initial_frame).run()

        simulation = Simulation(config, initial_frame)
        while not simulation.should_end():
            simulation.generate_next_frame()
            simulation.go_to_next_frame()

        return simulation.current_frame()
