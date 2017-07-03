import os

"""
Constants
"""

DEBUG = 1
WINDOW_NAME = 'Subtracted reality'

# Sets window and stream sizes
SIZE = (1280, 720)
# SIZE = (640, 480)

# CAMERA TYPE
# use 'pi' for PiCamera
# use int for web cam source
CAMERA = 0
FRAMERATE = 30

# BASE DIR AND DEFAULT BACKGROUND FILE
DIR = os.path.dirname(os.path.realpath(__file__))
BG_FILE = 'assets/test-card_640x480.png'
# BG_FILE = 'assets/sea_4-3.mov'

# COLOUR IN HSV
# HUE ranges from 0 - 179
# SAT, VAL range from 0 - 255
COLOUR_IN = [100, 100, 100]
COLOUR_OUT = [110, 255, 255]
