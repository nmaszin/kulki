import sys
import copy
import yaml
import json
import climmands
from datetime import datetime

from app.simulation.simulation import Simulation
from app.simulation.results import ResultsObtainer
from app.config import JsonConfigFile, SimulationConfig
from app.simulation.generator import FrameGenerator

class MultiSimulationCommand(climmands.Command):
    name = 'multisimulation'
    description = 'Perform multiple simulations for different balls number'

    def initialize_arguments_parser(self, parser):
        parser.add_argument('--config', help='Path to config file')

    def execute(self, parsed_arguments):
        config = self.obtain_config(parsed_arguments)
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
            last_frame = self.nonvisual_simulation(config, initial_frame)
            current_results = ResultsObtainer(last_frame).obtain()

            results[current_balls_number] = current_results

        print(json.dumps(results))

    def obtain_config(self, parsed_arguments):
        config_path = parsed_arguments.config

        if config_path is None:
            custom_user_config = {}
        else:
            custom_user_config = JsonConfigFile(config_path).read()

        return SimulationConfig(custom_user_config)

    def nonvisual_simulation(self, config, initial_frame):  
        simulation = Simulation(config, initial_frame)
        while not simulation.should_end():
            simulation.generate_next_frame()
            simulation.go_to_next_frame()

        return simulation.current_frame()