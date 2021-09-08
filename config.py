import random

def get_screen_size():
    """Get info about user screen width, height"""
    import pygame
    pygame.init()
    screen_info = pygame.display.Info()
    screen_width = screen_info.current_w
    screen_height = screen_info.current_h
    return screen_width, screen_height

# [CORE]
RANDOM_CELLS = True
RULE = "3/2,3"
RECORD = False
ENDGAME = 2  # 1 start new game, 2 add new cells, 3 clean field
NUMBER_OF_CELLS = random.uniform(0.1, 0.9) # 0 < num < 1 or random.uniform(0.1, 0.9)

# [FRONT]
FRONT = True
FPS = 10
CELL_SIZE = 10
FONT_SIZE = 25
EMPTY_CELLS = False  # True = empty borders, False = color filled

# [WINDOW]
WINDOW_WIDTH = get_screen_size()[0]
WINDOW_HEIGHT = get_screen_size()[1]
NAVBAR_WIDTH = int(WINDOW_WIDTH * 0.2)
FIELD_WIDTH = int(WINDOW_WIDTH * 0.75)
FIELD_HEIGHT = int(WINDOW_HEIGHT * 0.8)

# [RGB]
COLOR_LIVE = 61,182,61  # lime, cells 
COLOR_DEAD = 24,26,27  # black, background 
COLOR_LINE = 39, 42, 44  # gray, lines on field 
COLOR_INFO = 200, 200, 200  # white, top info
COLOR_NAVBAR = 50, 50, 50
