import sys
import pygame
from pygame.locals import *
import config

FONT_SIZE = config.FONT_SIZE

class GameWindow:

    FPS = config.FPS
    WIDTH = config.FIELD_WIDTH + config.NAVBAR_WIDTH
    HEIGHT = config.FIELD_HEIGHT

    def __init__(self):
        pygame.init()
        self.font_pygame = pygame.font.SysFont('Arial', FONT_SIZE)
        self.surface = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()

    
    def display_update(self):
        pygame.display.update()


    def check_events(self):
        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    return ['HOTKEY', (0, 0), 'SPACE']
                if event.key == K_e:
                    return['EMPTY_CELLS']

            if event.type == pygame.VIDEORESIZE:
                return['FULLSCREEN', (event.w, event.h)]

            elif event.type == MOUSEBUTTONDOWN:

                if event.button == 1:  
                    if event.pos[0] in range(config.FIELD_WIDTH) and event.pos[1] in range(config.FIELD_HEIGHT):
                        pos = (event.pos[0] // self.CELL_SIZE, event.pos[1] // self.CELL_SIZE)
                        return ['NEIGHBORS_UPDATE', pos]
                    return['LMC', event.pos]  # Left Mouse Click
                elif event.button == 2:  
                    return['SWC', event.pos]  # Scroll Wheel Press
                elif event.button == 3:
                    return['RMC', event.pos]
                elif event.button == 4:
                    return['SWU', event.pos]
                elif event.button == 5:
                    return['LMC', event.pos]              

        return 0



class Field:

    WIDTH = config.FIELD_WIDTH
    HEIGHT = config.FIELD_HEIGHT
    CELL_SIZE = config.CELL_SIZE
    COLOR_LIVE = config.COLOR_LIVE
    COLOR_DEAD = config.COLOR_DEAD

    def __init__(self):
        self.font_pygame = pygame.font.SysFont('Arial', FONT_SIZE)
        self.surface = pygame.Surface((self.WIDTH, self.HEIGHT))


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
                # pygame.draw.circle(
                #     self.surface, 
                #     self.COLOR_LIVE, 
                #     (cells[i].x * self.CELL_SIZE,
                #      cells[i].y * self.CELL_SIZE),
                #      self.CELL_SIZE // 2,

                #      config.EMPTY_CELLS)
                

    def draw_lines(self):
        for x in range(0, self.HEIGHT, self.CELL_SIZE):
            pygame.draw.line(
                self.surface, 
                config.COLOR_LINE,
                (0, x),
                (self.WIDTH, x))
            if x % (self.CELL_SIZE * 2)  == 0:  # 2 lines next to each other = bold line
                pygame.draw.line(
                    self.surface, 
                    config.COLOR_LINE,
                    (0, x+1),
                    (self.WIDTH, x+1))
    
        for y in range(0, self.WIDTH, self.CELL_SIZE):
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



class NavigationBar:

    WIDTH = config.NAVBAR_WIDTH
    HEIGHT = config.FIELD_HEIGHT
    COLOR_INFO = config.COLOR_INFO
    COLOR_BACKGROUND = config.COLOR_NAVBAR

    def __init__(self):
        self.font_pygame = pygame.font.SysFont('Arial', FONT_SIZE)
        self.surface = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()


    def draw_info(self, generation, live_cells, cells):
        
        self.surface.fill(self.COLOR_BACKGROUND)
        text_gen = self.font_pygame.render(
            "GENERATION: " + str(generation), 1, self.COLOR_INFO)
        text_count_cells = self.font_pygame.render(
            "ALIVE CELLS: " + str(live_cells), 1, self.COLOR_INFO)
        text_count_cells1 = self.font_pygame.render(
            "DEAD CELLS: " + str(abs(len(cells)-live_cells)), 1, self.COLOR_INFO)

        text_scale = self.font_pygame.render(
            "SCALE", 1, self.COLOR_INFO)
        text_speed = self.font_pygame.render(
            "FPS", 1, self.COLOR_INFO)
        self.surface.blit(text_scale, (config.NAVBAR_WIDTH * 0.35, config.NAVBAR_HEIGHT - config.NAVBAR_HEIGHT * 0.77))
        self.surface.blit(text_speed, (config.NAVBAR_WIDTH * 0.41, config.NAVBAR_HEIGHT - config.NAVBAR_HEIGHT * 0.67))

        left_space = int(config.NAVBAR_WIDTH * 0.05)
        top_space = int(config.NAVBAR_WIDTH * 0.05)

        self.surface.blit(text_gen, (left_space, top_space))
        self.surface.blit(text_count_cells, (left_space, top_space + FONT_SIZE))
        self.surface.blit(text_count_cells1, (left_space, top_space + FONT_SIZE*2))


    def blit_surfaces(self, surfaces):
        for surface_info in surfaces:
            surface = surface_info[0]
            x = surface_info[1]
            y = surface_info[2]
            self.surface.blit(surface, (x, y))





class Button():
    """Create a button, then blit the surface in the while loop"""

    def __init__(self, text: str, pos: tuple, font: int, size=(config.BUTTON_WIDTH, config.BUTTON_HEIGHT), bg="black", feedback=""):
        self.name = text
        self.x, self.y = pos
        self.width, self.height = size
        self.font = pygame.font.SysFont("Arial", font)
        if feedback == "":
            self.feedback = "text"
        else:
            self.feedback = feedback
        self.change_text(self.name, bg)


    def change_text(self, text, bg="black"):
        """Change the text when you click"""
        self.text = self.font.render(text, 1, pygame.Color("White"))
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(bg)
        self.surface.blit(self.text, (self.width // 2 - self.text.get_size()[0] // 2, self.height // 2 - self.text.get_size()[1] // 2))
        self.rect = pygame.Rect(config.FIELD_WIDTH + self.x, config.NAVBAR_HEIGHT - self.y, self.width, self.height)
        
