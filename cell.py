import random

class Cell:

    x: int
    y: int
    status: bool  # false - died, true - alive
    neighbors_count: int

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.status = False
        self.neighbors_count = 0
        # self.color = random.randint


    def dump(self):
        result = {"x": self.x, "y": self.y, "status": self.status, "neighbors_count": self.neighbors_count}
        return result

