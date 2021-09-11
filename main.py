from front import Field
import core
import config
import datetime
import random

FRONT = config.FRONT
if FRONT:
    import front
    WINDOW = front.GameWindow()
    FIELD = front.Field()
    NAVBAR = front.NavigationBar()

    btn_options = front.Button(
        "OPTIONS",
        (config.NAVBAR_WIDTH * 0.1, 
        config.NAVBAR_HEIGHT * 0.1),
        font=20,
        bg="black",
        feedback="<- BACK")

    btn_exit = front.Button(
        "EXIT",
        (100, 
        200),

        font=20,
        bg="black",
        feedback="ok")

# PLAY = not FRONT
PLAY = True
config.RECORD = True if not FRONT else config.RECORD

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
            print('2')
            FIELD.COLOR_LIVE = random.randint(100, 245), random.randint(100, 245), random.randint(100, 245)
            cell_auto.make_RANDOM_CELLS()
        elif ENDGAME == 3:  # clean field
            cell_auto.clean_cells()
        elif ENDGAME == 4:  # do nothing
            pass


def main_cycle():
    global PLAY
    finished = False
    while not finished:
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

        if FRONT:
            FIELD.surface.fill((FIELD.COLOR_DEAD))
            FIELD.draw_lines()
            FIELD.draw_cells(cell_auto.cells) 
            NAVBAR.draw_info(cell_auto.generation,
                        cell_auto.live_cells, cell_auto.cells)

        
            NAVBAR.blit_surface(btn_options.surface, 
                config.NAVBAR_WIDTH // 2 - btn_options.x // 2, 
                config.NAVBAR_HEIGHT - btn_options.y)

            NAVBAR.blit_surface(btn_exit.surface, 
                10, 20)


            WINDOW.blit_surface(FIELD.surface, 0, 0)
            WINDOW.blit_surface(NAVBAR.surface, FIELD.WIDTH, 0)

        
            WINDOW.display_update()

            result = FIELD.check_events()
            if result[0] == 'PLAY_UPDATE':
                print('play = not play')
                PLAY = not PLAY
            elif result[0] == 'NEIGHBORS_UPDATE':
                cell_auto.cells[result[1][1] + result[1][0] * cell_auto.HEIGHT].status = True if not cell_auto.cells[result[1][1] +
                                                                                                                    result[1][0] * cell_auto.HEIGHT].status else False
                cell_auto.update_neighbors()
            elif result[0] == 'EMPTY_CELLS':
                config.EMPTY_CELLS = not config.EMPTY_CELLS
            elif result[0] == 'BUTTON':
                print(result[1])
                print(btn_options.rect.x, btn_options.rect.y)
                if btn_options.rect.collidepoint(result[1]):
                    print('PRESS')
                    btn_options.change_text(btn_options.feedback, bg="red")


            # button1.show()


def main():
    main_cycle()


if __name__ == "__main__":
    main()
