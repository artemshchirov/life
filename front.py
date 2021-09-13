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
        self.surface = pygame.display.set_mode(
            (self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()

    
    def blit_surface(self, surface, x, y):
        self.surface.blit(surface, (x, y))

    
    def display_update(self):
        pygame.display.update()



class Field:

    WIDTH = config.FIELD_WIDTH
    HEIGHT = config.FIELD_HEIGHT
    CELL_SIZE = config.CELL_SIZE
    COLOR_LIVE = config.COLOR_LIVE
    COLOR_DEAD = config.COLOR_DEAD
    play = False

    def __init__(self):
        # pygame.init()
        self.font_pygame = pygame.font.SysFont('Arial', FONT_SIZE)
        # self.clock = pygame.time.Clock()
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


    def blit_surface(self, surface, x, y):
        self.surface.blit(surface, (x, y))


    def check_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    return ['PLAY_UPDATE']
                if event.key == K_e:
                    return['EMPTY_CELLS']
            elif event.type == MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                if pygame.mouse.get_pressed()[0]:
                    return['BUTTON', pygame.mouse.get_pos()]

                if x in range(config.FIELD_WIDTH) and y in range(config.FIELD_HEIGHT):
                    pos = (x // self.CELL_SIZE, y // self.CELL_SIZE)
                    return ['NEIGHBORS_UPDATE', pos]


            # button1.click(event)

        return ['']



class NavigationBar:

    WIDTH = config.NAVBAR_WIDTH
    HEIGHT = config.FIELD_HEIGHT
    COLOR_INFO = config.COLOR_INFO
    COLOR_BACKGROUND = config.COLOR_NAVBAR

    def __init__(self):
        # pygame.init()
        self.font_pygame = pygame.font.SysFont('Arial', FONT_SIZE)
        # self.clock = pygame.time.Clock()
        self.surface = pygame.Surface((self.WIDTH, self.HEIGHT))


    def draw_info(self, generation, live_cells, cells):
        
        self.surface.fill(self.COLOR_BACKGROUND)
        text_gen = self.font_pygame.render(
            "GENERATION: " + str(generation), 1, self.COLOR_INFO)
        text_count_cells = self.font_pygame.render(
            "ALIVE CELLS: " + str(live_cells), 1, self.COLOR_INFO)
        text_count_cells1 = self.font_pygame.render(
            "DEAD CELLS: " + str(abs(len(cells)-live_cells)), 1, self.COLOR_INFO)

        left_space = int(config.NAVBAR_WIDTH * 0.05)
        top_space = int(config.NAVBAR_WIDTH * 0.05)

        self.surface.blit(text_gen, (left_space, top_space))
        self.surface.blit(text_count_cells, (left_space, top_space + FONT_SIZE))
        self.surface.blit(text_count_cells1, (left_space, top_space + FONT_SIZE*2))

    def blit_surface(self, surface, x, y):
        self.surface.blit(surface, (x, y))



class Button():
    """Create a button, then blit the surface in the while loop"""

    def __init__(self, text: str, pos: tuple, font: int, bg="black", feedback=""):
        self.x, self.y = pos
        self.font = pygame.font.SysFont("Arial", font)
        if feedback == "":
            self.feedback = "text"
        else:
            self.feedback = feedback
        self.change_text(text, bg)



    def change_text(self, text, bg="black"):
        """Change the text whe you click"""
        print("PRESSED")
        self.text = self.font.render(text, 1, pygame.Color("White"))
        # self.size = self.text.get_size() 
        self.surface = pygame.Surface((config.BUTTON_WIDTH, config.BUTTON_HEIGHT))
        self.surface.fill(bg)
        self.surface.blit(self.text, (config.BUTTON_WIDTH // 2 - self.text.get_size()[0] // 2, config.BUTTON_HEIGHT // 2 - self.text.get_size()[1] // 2))
        self.rect = pygame.Rect(config.FIELD_WIDTH + self.x, config.NAVBAR_HEIGHT - self.y, config.BUTTON_WIDTH, config.BUTTON_HEIGHT)
        # print(f"Rect {self.text} coords: {config.FIELD_WIDTH + self.x, config.NAVBAR_HEIGHT - self.y}")
    
    # def show(self):
    #     self.surface.blit(self.surface, (self.x, self.y))

    # def click(self, event):
    #     x, y = pygame.mouse.get_pos()
    #     if event.type == pygame.MOUSEBUTTONDOWN:
    #         if pygame.mouse.get_pressed()[0]:
    #             if self.rect.collidepoint(x, y):
    #                 self.change_text(self.feedback, bg="red")

