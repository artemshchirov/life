import sys
import pygame
from pygame.locals import *
import config

FONT_SIZE = config.FONT_SIZE

class Field:

    FPS = config.FPS
    WIDTH = config.FIELD_WIDTH
    HEIGHT = config.FIELD_HEIGHT
    CELL_SIZE = config.CELL_SIZE
    COLOR_LIVE = config.COLOR_LIVE
    COLOR_DEAD = config.COLOR_DEAD

    play = False

    def __init__(self):
        pygame.init()
        self.font_pygame = pygame.font.SysFont('Arial', FONT_SIZE)
        self.surface = pygame.display.set_mode(
            (self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()


    def draw_cells(self, cells):
        for i in range(len(cells)):
            if cells[i].status:
                pygame.draw.rect(
                    self.surface, 
                    self.COLOR_LIVE, 
                    (cells[i].x * self.CELL_SIZE,
                     cells[i].y * self.CELL_SIZE,
                     self.CELL_SIZE,
                     self.CELL_SIZE),
                     config.EMPTY_CELLS)
                

    def draw_lines(self):
        """
        """
        
        for x in range(0, self.HEIGHT, self.CELL_SIZE):
            pygame.draw.line(
                self.surface, 
                config.COLOR_LINE,
                (0, x),
                (self.WIDTH - config.NAVBAR_WIDTH, x))

            if x % (self.CELL_SIZE * 2)  == 0:  # 2 lines next to each other = bold line
                pygame.draw.line(
                    self.surface, 
                    config.COLOR_LINE,
                    (0, x+1),
                    (self.WIDTH - config.NAVBAR_WIDTH, x+1))

        for y in range(0, self.WIDTH - config.NAVBAR_WIDTH, self.CELL_SIZE):
            pygame.draw.line(
                self.surface, 
                config.COLOR_LINE, 
                (y, 0),
                (y, self.HEIGHT))

            if y % (self.CELL_SIZE * 2)  == 0:  
                pygame.draw.line(
                    self.surface, 
                    config.COLOR_LINE,
                    (y+1, 0),
                    (y+1, self.HEIGHT))


    def check_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    return ['PLAY_UPDATE']
                if event.key == K_e:
                    if config.EMPTY_CELLS:
                        return['FILL_CELLS']
                    else:
                        return ['EMPTY_CELLS']
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                pos = (pos[0] // self.CELL_SIZE, pos[1] // self.CELL_SIZE)
                return ['NEIGHBORS_UPDATE', pos]
        return ['']


    def display_update(self):
        pygame.display.update()



class NavigationBar:

    WIDTH = config.NAVBAR_WIDTH
    HEIGHT = config.FIELD_HEIGHT
    COLOR_INFO = config.COLOR_INFO
    COLOR_BACKGROUND = config.COLOR_DEAD

    def __init__(self):
        pygame.init()
        self.font_pygame = pygame.font.SysFont('Arial', FONT_SIZE)
        self.surface = Field.surface
        self.clock = pygame.time.Clock()

    def draw_info(self, generation, live_cells, cells):
        info_sc = pygame.Surface((300, self.WIDTH//2))
        info_sc.fill(self.COLOR_BACKGROUND)
        text_gen = self.font_pygame.render(
            "GENERATION: " + str(generation), 1, self.COLOR_INFO)
        text_count_cells = self.font_pygame.render(
            "ALIVE CELLS: " + str(live_cells), 1, self.COLOR_INFO)
        text_count_cells1 = self.font_pygame.render(
            "DEAD CELLS: " + str(abs(len(cells)-live_cells)), 1, self.COLOR_INFO)

        info_sc.blit(text_gen, (0, 0))
        info_sc.blit(text_count_cells, (0, FONT_SIZE))
        info_sc.blit(text_count_cells1, (0, FONT_SIZE*2))

        self.surface.blit(info_sc, (self.WIDTH, 0))