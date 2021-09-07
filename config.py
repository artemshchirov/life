import random


# [CORE]
RANDOM_CELLS = True
RULE = "3/2,3"
RECORD = False
ENDGAME = 2  # 1 start new game, 2 add new cells, 3 clean field
NUMBER_OF_CELLS = 0.1 # 0 < num < 1 or random.uniform(0.1, 0.9)


# [FRONT]
FRONT = True
FPS = 120

FIELD_WIDTH = 900
FIELD_HEIGHT = 700
NAVBAR_WIDTH = 300

CELL_SIZE = 10
FONT_SIZE = 30
EMPTY_CELLS = False  # True = empty borders, False = color filled

# [RGB]
COLOR_LIVE = 61,182,61  # lime, cells 
COLOR_DEAD = 24,26,27  # black, background 
COLOR_LINE = 39, 42, 44  # gray, lines on field 
COLOR_INFO = 200, 200, 200  # white, top info
COLOR_NAVBAR = 50, 50, 50


