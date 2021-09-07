import core
import config
import datetime
import random


FRONT = config.FRONT
if config.FIELD_WIDTH > 1500:
    FRONT = False
if FRONT:
    import front
    # NAV_bar = front.NavigationBar()
    FRONT_game = front.Field()


PLAY = not FRONT
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
            FRONT_game.LIVE_COLOR = random.randint(50, 225), random.randint(50, 225), random.randint(50, 225)
            cell_auto.make_RANDOM_CELLS()
        elif ENDGAME == 3:  # clean field
            cell_auto.clean_cells()


def main_cycle():
    global PLAY
    while True:
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
            FRONT_game.clock.tick(FRONT_game.FPS)
            FRONT_game.display_update()
            FRONT_game.surface.fill((FRONT_game.COLOR_DEAD))

            FRONT_game.draw_lines()

            FRONT_game.draw_cells(cell_auto.cells)

            result = FRONT_game.check_events()

            # NAV_bar.draw_info(cell_auto.generation,
            #             cell_auto.live_cells, cell_auto.cells)

            if result[0] == 'PLAY_UPDATE':
                PLAY = not PLAY
            elif result[0] == 'NEIGHBORS_UPDATE':
                cell_auto.cells[result[1][1] + result[1][0] * cell_auto.WIDTH].status = True if not cell_auto.cells[result[1][1] +
                                                                                                                    result[1][0] * cell_auto.WIDTH].status else False
                cell_auto.update_neighbors()
            elif result[0] == 'EMPTY_CELLS':
                config.EMPTY_CELLS = True
            elif result[0] == 'FILL_CELLS':
                config.EMPTY_CELLS = False


def main():
    main_cycle()


if __name__ == "__main__":
    main()