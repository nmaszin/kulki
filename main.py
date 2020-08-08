#!/usr/bin/env python3

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

import argparse
import climmands

from app.app import App
from app.commands import *

def main():
    parser = argparse.ArgumentParser(description='Kulki by NMaszin')
    commands = climmands.CommandLoader(parser).load_commands()
    executor = climmands.CommandExecutor(commands)

    parsed_arguments = parser.parse_args()
    if not executor.execute(parsed_arguments):
        parser.print_help()

if __name__ == '__main__':
    main()