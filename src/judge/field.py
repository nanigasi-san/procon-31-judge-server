from random import randint
from typing import Tuple

Point = Tuple[int, int]


class Field:
    def __init__(self, size: Point):
        self.height, self.width = size
        self.base_point = [[randint(-16, 16) for _ in range(self.width)] for _ in range(self.height)]
        self.status = [["*" for _ in range(self.width)] for _ in range(self.height)]
