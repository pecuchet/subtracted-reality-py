import os

"""
Constants
"""

DEBUG = 1
SIZE = (640, 480)
#SIZE = (960, 720)
#SIZE = (1280, 960)
WINDOW_NAME = 'Subtracted reality'
DIR = os.path.dirname(os.path.realpath(__file__))

# COLOUR IN HSV
# HUE ranges from 0 - 179
# SAT, VAL range from 0 - 255
COLOUR_IN = [100, 100, 100]
COLOUR_OUT = [110, 255, 255]
