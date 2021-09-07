import random
import config
from cell import Cell

class CellularAutomation:
    
    CELL_SIZE = config.CELL_SIZE
    WIDTH = config.FIELD_WIDTH // CELL_SIZE
    cells: dict
    last_snapshot = {}
    generation = 0
    live_cells = 0    
    RULE = config.RULE  # source

    def __init__(self):
        self.cells = {
            j + self.WIDTH * i: Cell(i, j) for i in range(self.WIDTH) for j in range(self.WIDTH)}
        
        if config.RANDOM_CELLS:
            self.clean_cells()
            self.make_RANDOM_CELLS()


    def make_RANDOM_CELLS(self):
        """Create new cells"""
        cells = int(len(self.cells) * config.NUMBER_OF_CELLS)
        for _ in range(cells): 
            random_id = random.randint(0, len(self.cells) - 1)
            self.cells[random_id].status = True
        self.update_neighbors()


    def update_neighbors(self):
        for curr_cell in self.cells.keys():
            self.cells[curr_cell].neighbors_count = self.get_neighbors_count(self.cells[curr_cell].x,
                                                                             self.cells[curr_cell].y)


    def get_neighbors_count(self, current_x: int, current_y: int) -> int:
        count = 0
        for i in range(current_x - 1, current_x + 2):
            for j in range(current_y - 1, current_y + 2):
                if (i == current_x) and (j == current_y):
                    pass
                else:
                    if i < 0:
                        i = self.WIDTH - 1
                    elif i > self.WIDTH:
                        i = 0

                    if j < 0:
                        j = self.WIDTH - 1
                    elif j > self.WIDTH:
                        j = 0

                    curr_id = j + self.WIDTH * i
                    try:
                        if self.cells[curr_id].status:
                            count += 1
                    except:
                        pass
        return count


    def update_cells(self):
        RULE_sections = self.RULE.split('/')
        b = RULE_sections[0].split(',')
        s = RULE_sections[1].split(',')
        for key, item in self.cells.items():
            if self.cells[key].status:
                if not (str(item.neighbors_count) in s):
                    self.cells[key].status = False
            else:
                if str(item.neighbors_count) in b:
                    self.cells[key].status = True


    def clean_cells(self):
        self.cells = {
            j + self.WIDTH * i: Cell(i, j) for i in range(self.WIDTH) for j in range(self.WIDTH)}


    def calculate_cells(self):
        self.live_cells = 0
        for cell in self.cells.values():
            if cell.status:
                self.live_cells += 1
