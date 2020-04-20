from random import randint
from typing import List, NamedTuple, Tuple, Iterable, TypeVar
from itertools import chain


class Point(NamedTuple):
    x: int
    y: int

    def update(self, diff: Tuple[int, int]) -> "Point":
        return Point(self.x + diff[0], self.y + diff[1])

    @staticmethod
    def gen_all_points(height: int, width: int) -> Iterable["Point"]:
        unflatten_all_points = [[Point(x, y) for y in range(width)] for x in range(height)]
        return chain.from_iterable(unflatten_all_points)


T = TypeVar("T", int, str)


class Grid(List[List[T]]):
    def __init__(self, grid: List[List[T]]):
        for line in grid:
            self.append(line)

    def at(self, point: Point) -> T:
        return self[point.x][point.y]


class Field:
    def __init__(self, size: Tuple[int, int]):
        self.size = size
        self.height, self.width = size
        self.base_point = Grid([[randint(-16, 16) for _ in range(self.width)] for _ in range(self.height)])
        self.status = Grid([["*" for _ in range(self.width)] for _ in range(self.height)])
