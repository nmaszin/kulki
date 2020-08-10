import climmands
from datetime import datetime

from app.app import App
from app.simulation.file import FrameFile
from app.config import SimulationConfig, YamlConfigFile
from app.simulation.generator import FrameGenerator

from app.math.vector import Vector

class DemoCommand(climmands.Command):
    name = 'demo'
    description = 'Run a demo'

    def initialize_arguments_parser(self, parser):
        self.parser = parser
        parser.add_argument('--config', help='Path to custom config file')
        subparsers = parser.add_subparsers(dest='action')
        
        save_parser = subparsers.add_parser('save', help='Save simulation to file')
        save_parser.add_argument('file', nargs='?', help='Simulation file')

        load_parser = subparsers.add_parser('load', help='Load demo from file')
        load_parser.add_argument('file', help='Simulation file')

    def execute(self, parsed_arguments):
        config = self.obtain_config(parsed_arguments)
        frame = self.obtain_frame(config, parsed_arguments)        

        app = App(config, frame)
        app.run()
    
    def obtain_frame(self, config, parsed_arguments):
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