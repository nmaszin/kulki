import yaml
import climmands
from datetime import datetime

from app.app import App
from app.simulation.file import FrameFile
from app.config import SimulationConfig
from app.simulation.generator import FrameGenerator
from app.config import YamlConfigFile, SimulationConfig

from app.math.vector import Vector

class SimulationCommand(climmands.Command):
    name = 'simulation'
    description = 'Run a simulation'

    def initialize_arguments_parser(self, parser):
        parser.add_argument('--config', help='Path to config file')

    def execute(self, parsed_arguments):
        config = self.obtain_config(parsed_arguments)

        for entry, value in config.all().items():
            print(f'{entry} = {value}')

    def obtain_config(self, parsed_arguments):
        config_path = parsed_arguments.config

        if config_path is None:
            custom_user_config = {}
        else:
            custom_user_config = YamlConfigFile(config_path).read()

        return SimulationConfig(custom_user_config)
