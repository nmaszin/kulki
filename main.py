#!/usr/bin/env python3

from app.commands import *
import climmands
import argparse
import signal
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

signal.signal(signal.SIGINT, signal.default_int_handler)


def main():
    parser = argparse.ArgumentParser(description='Kulki by NMaszin')
    commands = climmands.CommandLoader(parser).load_commands()
    executor = climmands.CommandExecutor(commands)

    parsed_arguments = parser.parse_args()
    if not executor.execute(parsed_arguments):
        parser.print_help()


if __name__ == '__main__':
    main()
