import sys
import json
import climmands
from datetime import datetime
import matplotlib.pyplot as pyplot

from app.json_file import JsonFile


class PlotCommand(climmands.Command):
    name = 'plot'
    description = 'Plot results'

    results_names = {
        'collisions_counter': 'Liczba kolizji',
        'average_free_path': 'Średnia droga swobodna',
    }

    def initialize_arguments_parser(self, parser):
        parser.add_argument('results', help='Path to file with results')

    def execute(self, parsed_arguments):
        results = JsonFile(parsed_arguments.results).read()

        transformed_results = {}
        for x_value, stats in results.items():
            stats = stats[0]  # We handle only the first tracked ball
            for prop, y_value in stats.items():
                if prop not in transformed_results:
                    transformed_results[prop] = {'x': [], 'y': []}

                transformed_results[prop]['x'].append(x_value)
                transformed_results[prop]['y'].append(y_value)

        for prop, data in transformed_results.items():
            name = self.results_names.get(prop, prop)
            self.plot(name, 'N', name, data['x'], data['y'])

    def plot(self, title, legend_x, legend_y, x_values, y_values):
        pyplot.figure(num=title)
        pyplot.title(title)
        pyplot.xlabel(legend_x)
        pyplot.ylabel(legend_y)
        pyplot.plot(x_values, y_values, 'b--', label=title)
        pyplot.legend(loc='upper left')
        pyplot.show()
