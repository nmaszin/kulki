import sys
import yaml
import json
import climmands
from datetime import datetime
import matplotlib.pyplot as pyplot

from app.config import ConfigObtainer

class PlotCommand(climmands.Command):
    name = 'plot'
    description = 'Plot results'

    def initialize_arguments_parser(self, parser):
        parser.add_argument('--config', help='Path to config file')

    def execute(self, parsed_arguments):
        config = ConfigObtainer(parsed_arguments.config).obtain()
        results = json.load(sys.stdin)

        transformed_results = {}
        for x_value, stats in results.items():
            stats = stats[0] # We handle only the first tracked ball
            for prop, y_value in stats.items():
                if prop not in transformed_results:
                    transformed_results[prop] = {'x': [], 'y': []}
                
                transformed_results[prop]['x'].append(x_value)
                transformed_results[prop]['y'].append(y_value)

        for prop, data in transformed_results.items():
            self.plot(prop, 'N', prop, data['x'], data['y'])

    def plot(self, title, legend_x, legend_y, x_values, y_values):
        pyplot.figure(num=title)
        pyplot.title(title)
        pyplot.xlabel(legend_x)
        pyplot.ylabel(legend_y)
        pyplot.plot(x_values, y_values, 'b--', label=title)
        pyplot.legend(loc='upper left')
        pyplot.show()