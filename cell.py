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
        # self.color = random.choice([COLORS])


    def dump(self):
        # print(f"x: {self.x}, y: {self.y}, status: {self.status}, neighbors_count: {self.neighbors_count}")
        result = {"x": self.x, "y": self.y, "status": self.status, "neighbors_count": self.neighbors_count}
        # print("return result", result)
        return result

# c1 = Cell(1, 4)
# c1.dump()
# c2 = Cell(23, 47)
# c1.dump()