"""
Ten moduł pozwala w prosty sposób importować moduły wszystkich komend
poprzez składnię: from app.commands import *

W liście __all__ określane są wszystkie podmoduły, które mają w takim przypadku zostać zaimportowane
"""

__all__ = [
    'simulation',
    'multisimulation',
    'plot'
]
