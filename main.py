import pygame
import config
import front
import core
import cell
import datetime
from random import randint
import sys

if config.FRONT:
    WINDOW = front.GameWindow()
    FIELD = front.Field()
    NAVBAR = front.NavigationBar()

    nav_w = config.NAVBAR_WIDTH
    nav_h = config.NAVBAR_HEIGHT
    btn_w = config.BUTTON_WIDTH
    btn_h = config.BUTTON_HEIGHT
    btn_f = config.BUTTON_FONT_SIZE

    btn_scale_plus = front.Button("+", (nav_w * .735, nav_h * .66), (btn_w // 3.2, btn_h / 1.7), btn_f)
    btn_speed_plus = front.Button("+", (nav_w * .735, nav_h * .6), (btn_w // 3.2, btn_h / 1.7), btn_f)

    btn_scale_minus = front.Button("-", (nav_w * .15, nav_h * .66), (btn_w // 3.2, btn_h / 1.7), btn_f)
    btn_speed_minus = front.Button("-", (nav_w * .15, nav_h * .6), (btn_w // 3.2, btn_h /1.7), btn_f)

    btn_start = front.Button("START", (nav_w * .05, nav_h * .5), (nav_w * .4525, nav_h * .09), btn_f ,bg="green4",feedback="PAUSE")
    btn_step = front.Button("STEP", (nav_w * .5225, nav_h * .5), (nav_w * .4525, nav_h * .09), btn_f)

    btn_add_cells = front.Button("ADD", (nav_w * .74, nav_h * .4), (btn_w // 1.8, btn_h), btn_f)
    btn_del_cells = front.Button("DEL", (nav_w * .05, nav_h * .4), (btn_w // 1.8, btn_h), btn_f)
    btn_reset = front.Button("RESET", (nav_w * .3, nav_h * .4), (btn_w, btn_h), btn_f)
    
    btn_help = front.Button("HELP", (nav_w * .05, nav_h * .2), (nav_w * .4525, nav_h * .09), btn_f)
    btn_fullscreen = front.Button("SCREEN", (nav_w * .5225, nav_h * .2), (nav_w * .4525, nav_h * .09), btn_f)
    
    btn_exit = front.Button("EXIT", (nav_w * .5225, nav_h * .1), (nav_w * .4525, nav_h * .09), btn_f)
    btn_options = front.Button("OPTIONS", (nav_w * .05, nav_h * .1), (nav_w * .4525, nav_h * .09), btn_f, feedback="<- BACK")

config.RECORD = True if not config.FRONT else config.RECORD

if config.RECORD:
    f = open('record.log', 'w')

cell_auto = core.CellularAutomation()

def write_log(delta_time):
    if config.RECORD:
        s = f'{cell_auto.live_cells}/{abs(len(cell_auto.cells)-cell_auto.live_cells)}/{delta_time}'
        f.write(s+'\n')
        print(s+f'\tGEN: {cell_auto.generation}\t DELTA_TIME: {delta_time}')


def check_endgame():
    """What happenes when all cells don`t move or alive"""
    ENDGAME = config.ENDGAME
    if cell_auto.last_snapshot == cell_auto.live_cells or cell_auto.live_cells == 0:
        if ENDGAME == 1:  # start new game
            cell_auto.clean_cells()
            cell_auto.make_RANDOM_CELLS()
        elif ENDGAME == 2:  # add new cells
            if not config.COLOR_CELLS_RANDOM:
                config.COLOR_LIVE = randint(0, 255), randint(0, 255), randint(0, 255)
                
            cell_auto.make_RANDOM_CELLS()
        elif ENDGAME == 3:  # clean field
            cell_auto.clean_cells()
        elif ENDGAME == 0:  # do nothing
            pass

def NAVBAR_surfaces_main():
    surfaces = [
    # GAME INFO

    # BUTTONS INFO

    # BUTTONS
        [btn_options.surface, btn_options.x, config.NAVBAR_HEIGHT - btn_options.y],
        [btn_exit.surface, btn_exit.x, config.NAVBAR_HEIGHT - btn_exit.y],
        [btn_add_cells.surface,btn_add_cells.x,config.NAVBAR_HEIGHT - btn_add_cells.y],
        [btn_del_cells.surface,btn_del_cells.x,config.NAVBAR_HEIGHT - btn_del_cells.y],
        [btn_scale_plus.surface,btn_scale_plus.x,config.NAVBAR_HEIGHT - btn_scale_plus.y],
        [btn_scale_minus.surface,btn_scale_minus.x,config.NAVBAR_HEIGHT - btn_scale_minus.y],
        [btn_speed_plus.surface,btn_speed_plus.x,config.NAVBAR_HEIGHT - btn_speed_plus.y],
        [btn_speed_minus.surface,btn_speed_minus.x,config.NAVBAR_HEIGHT - btn_speed_minus.y],
        [btn_reset.surface,btn_reset.x,config.NAVBAR_HEIGHT - btn_reset.y],
        [btn_step.surface,btn_step.x,config.NAVBAR_HEIGHT - btn_step.y],
        [btn_start.surface,btn_start.x,config.NAVBAR_HEIGHT - btn_start.y],        
        [btn_fullscreen.surface,btn_fullscreen.x,config.NAVBAR_HEIGHT - btn_fullscreen.y],
        [btn_help.surface,btn_help.x,config.NAVBAR_HEIGHT - btn_help.y],
        [btn_options.surface,btn_options.x,config.NAVBAR_HEIGHT - btn_options.y],
    ]   
    return surfaces

def NAVBAR_surfaces_options():
    """Return list with surfaces that displayed on sidebar when click on button OPTIONS"""
    surfaces = [
        [btn_options.surface, btn_options.x, config.NAVBAR_HEIGHT - btn_options.y],
        [btn_exit.surface, btn_exit.x, config.NAVBAR_HEIGHT - btn_exit.y],
        [btn_fullscreen.surface,btn_fullscreen.x,config.NAVBAR_HEIGHT - btn_fullscreen.y],
        [btn_help.surface,btn_help.x,config.NAVBAR_HEIGHT - btn_help.y],
    ]
    return surfaces

def get_screen_size():
    """Get info about user screen width, height"""
    pygame.init()
    screen_info = pygame.display.Info()
    screen_width = screen_info.current_w
    screen_height = screen_info.current_h
    return screen_width, screen_height

def set_style(default: int):
    result = default

    if config.CELL_STYLE == "random":
        result = 0
    elif config.CELL_STYLE == "rectangle":
        result = 1
    elif config.CELL_STYLE == "circle":
        result = 2
    
    return result

def main_cycle():

    PLAY = False
    options = False

    cell_styles = {"random":0, "rectangle":1, "circle":2}
    cell_style = set_style(cell_styles["rectangle"])


    running = True
    while running:
        WINDOW.clock.tick(config.FPS)
        if PLAY:
            cell_auto.generation += 1
            start_time = datetime.datetime.now()
            cell_auto.calculate_cells()
            cell_auto.update_cells()
            cell_auto.update_neighbors()
            if cell_auto.generation % 200 == 0:
                cell_auto.last_snapshot = cell_auto.live_cells
            else:
                check_endgame()
            end_time = datetime.datetime.now()
            delta_time = (end_time - start_time)
            write_log(f'{delta_time.seconds}.{delta_time.microseconds}')

        if config.FRONT:

            FIELD.surface.fill(config.COLOR_DEAD)
            FIELD.draw_lines()
            FIELD.draw_cells(cell_auto.cells) 
            NAVBAR.draw_info(cell_auto.generation,
                        cell_auto.live_cells, cell_auto.cells)
            if options:
                NAVBAR.blit_surfaces(NAVBAR_surfaces_options())
            else:
                NAVBAR.blit_surfaces(NAVBAR_surfaces_main())

            WINDOW.surface.blit(FIELD.surface, (0, 0))
            WINDOW.surface.blit(NAVBAR.surface, (FIELD.WIDTH, 0))
            WINDOW.display_update()

            result =  WINDOW.check_events()
            if result:
                print(result)

                if result[0] == 'FULLSCREEN':
                    WINDOW.surface = pygame.display.set_mode((result[1][0], result[1][1]),
                                pygame.RESIZABLE)

                elif result[0] == 'NEIGHBORS_UPDATE':
                    cell_auto.cells[result[1][1] + result[1][0] * cell_auto.HEIGHT].status = True if not cell_auto.cells[result[1][1] +
                                                                                                                        result[1][0] * cell_auto.HEIGHT].status else False
                    cell_auto.update_neighbors()

                elif result[0] == 'CHANGE_STYLE':
                    cell_style += 1
                    if cell_style > 2:
                        cell_style = 0
                    config.CELL_STYLE = list(cell_styles.keys())[list(cell_styles.values()).index(cell_style)]

                elif result[0] == 'CELL_RANDOM_COLOR':
                    config.CELL_COLOR_RANDOM = not config.CELL_COLOR_RANDOM

                elif result[0] == 'EMPTY_CELLS':
                    config.EMPTY_CELLS = not config.EMPTY_CELLS
                
                elif result[0] == 'LMC' or result[0] == 'HOTKEY':

                    if btn_start.rect.collidepoint(result[1]) or 'SPACE' in result:
                        PLAY = not PLAY
                        if PLAY:
                            btn_start.change_text(btn_start.feedback, bg="darkorange3")
                        else:
                            btn_start.change_text(btn_start.name, bg="green4")

                    elif btn_reset.rect.collidepoint(result[1]):
                        config.COLOR_LIVE = randint(0, 255), randint(0, 255), randint(0, 255)
                        cell_auto.clean_cells()
                        cell_auto.make_RANDOM_CELLS()

                    elif btn_add_cells.rect.collidepoint(result[1]):
                        cell_auto.make_RANDOM_CELLS()

                    elif btn_del_cells.rect.collidepoint(result[1]):
                        cell_auto.clean_cells()
                        if PLAY:
                            PLAY = False
                            btn_start.change_text(btn_start.name, bg="green4")

                    elif btn_scale_plus.rect.collidepoint(result[1]):
                        if PLAY:
                            PLAY = False
                            btn_start.change_text(btn_start.name, bg="green4")

                        FIELD.CELL_SIZE += 1
                        cell_auto.CELL_SIZE += 1
                        config.CELL_SIZE += 1
                        cell_auto.WIDTH = config.FIELD_WIDTH // config.CELL_SIZE
                        cell_auto.HEIGHT = config.FIELD_HEIGHT // config.CELL_SIZE
                        cell_auto.cells = {
                            j + cell_auto.HEIGHT * i: cell.Cell(i, j) for i in range(cell_auto.WIDTH) for j in range(cell_auto.HEIGHT)}
                        cell_auto.make_RANDOM_CELLS()
                        print(f"config.CELL_SIZE: {config.CELL_SIZE}")

                    elif btn_scale_minus.rect.collidepoint(result[1]):
                        if PLAY:
                            PLAY = False
                            btn_start.change_text(btn_start.name, bg="green4")
                            
                        FIELD.CELL_SIZE -= 1
                        cell_auto.CELL_SIZE -= 1
                        if config.CELL_SIZE > 1:
                            config.CELL_SIZE -= 1
                        else:
                            config.CELL_SIZE = 1
                        cell_auto.WIDTH = config.FIELD_WIDTH // config.CELL_SIZE
                        cell_auto.HEIGHT = config.FIELD_HEIGHT // config.CELL_SIZE
                        cell_auto.cells = {
                            j + cell_auto.HEIGHT * i: cell.Cell(i, j) for i in range(cell_auto.WIDTH) for j in range(cell_auto.HEIGHT)}
                        cell_auto.make_RANDOM_CELLS()
                        print(f"config.CELL_SIZE: {config.CELL_SIZE}")

                    elif btn_speed_plus.rect.collidepoint(result[1]):
                        config.FPS += 2  
                        print(f"FPS: {config.FPS}")

                    elif btn_speed_minus.rect.collidepoint(result[1]):
                        if config.FPS > 2:
                            config.FPS -= 2
                        else:
                            config.FPS = 2
                        print(f"FPS: {config.FPS}")

                    elif btn_step.rect.collidepoint(result[1]):
                        PLAY = False
                        cell_auto.generation += 1
                        cell_auto.calculate_cells() 
                        cell_auto.update_cells()
                        cell_auto.update_neighbors()

                    elif btn_help.rect.collidepoint(result[1]):
                        pass

                    elif btn_fullscreen.rect.collidepoint(result[1]):
                        fullscreen = True
                        
                        WINDOW.surface = pygame.display.set_mode((0, 0),
                                pygame.FULLSCREEN)

                        btn_fullscreen.change_text(btn_fullscreen.feedback, bg="red")

                    elif btn_options.rect.collidepoint(result[1]):
                        options = not options
                        if options:
                            btn_options.change_text(btn_options.feedback, bg="grey40")
                        else:
                            btn_options.change_text(btn_options.feedback, bg="black")

                    elif btn_exit.rect.collidepoint(result[1]):
                        pygame.quit()
                        sys.exit()



def main():
    print(f"FPS: {config.FPS}")
    main_cycle()


if __name__ == "__main__":
    main()
