import climmands
from app.app import App

class DemoCommand(climmands.Command):
    name = 'demo'
    description = 'Run a demo'

    def initialize_arguments_parser(self, parser):
        pass

    def execute(self, parsed_arguments):
        app = App()
        app.run()