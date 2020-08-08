import climmands
from datetime import datetime

from app.app import App
from app.simulation.file import FrameFile
from app.config import SimulationConfig
from app.simulation.generator import FrameGenerator

class DemoCommand(climmands.Command):
    name = 'demo'
    description = 'Run a demo'

    config = SimulationConfig({
        'width': 600,
        'height': 600,
        'fps': 60,
        'engine_fps': 60
    })

    def initialize_arguments_parser(self, parser):
        self.parser = parser
        subparsers = parser.add_subparsers(dest='action')
        
        save_parser = subparsers.add_parser('save', help='Save simulation to file')
        save_parser.add_argument('file', nargs='?', help='Simulation file')

        load_parser = subparsers.add_parser('load', help='Load demo from file')
        load_parser.add_argument('file', help='Simulation file')

    def execute(self, parsed_arguments):
        if parsed_arguments.action == 'load':
            frame = FrameFile(parsed_arguments.file).read()
        elif parsed_arguments.action == 'save':
            frame = FrameGenerator(self.config).generate()
            filename = parsed_arguments.file or self.__generate_simulation_filename()
            FrameFile(filename).write(frame)
        else:
            frame = FrameGenerator(self.config).generate()

        app = App(self.config, frame)
        app.run()
    
    def __generate_simulation_filename(self):
        time_string = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        extension = 'sim'
        return f'{time_string}.{extension}'