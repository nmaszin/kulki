#!/usr/bin/env python3

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

from app.app import App

app = App()
app.run()
