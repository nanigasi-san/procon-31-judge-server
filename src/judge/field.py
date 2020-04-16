from random import randint
from typing import Tuple as tuple


class Field:
    def __init__(self, size: tuple, *team: list):
        self.height, self.width = size
        self.base_point = [[randint(-16, 16) for _ in range(self.width)] for _ in range(self.height)]
        self.status = [["*" for _ in range(self.width)] for _ in range(self.height)]
        self.team = team

    def calc_point(self):
        points = [0, 0]
        for x in range(self.height):
            for y in range(self.width):
                cell = self.status[x][y]
                if cell == "*":
                    pass
                elif cell == "O":
                    points[0] += self.base_point[x][y]
                elif cell == "X":
                    points[1] += self.base_point[x][y]
                elif cell == "+":
                    points[0] += abs(self.base_point[x][y])
                elif cell == "-":
                    points[1] += abs(self.base_point[x][y])
                else:
                    raise CellError("this cell({0}, {1}) has \"{2}\". It is not supposed status.".format(x, y, cell))

        return {team_name: point for team_name, point in zip(self.team, points)}

    def fill(self, marker: tuple, tops: tuple[tuple[int]]):
        tops = list(tops)
        start = tops.pop(0)
        while tops:
            target = tops.pop(0)
            if start[0] == target[0]:
                if target[1] >= start[1]:
                    for dy in range(target[1] - start[1] + 1):
                        self.status[start[0]][start[1] + dy] = marker[0]
                else:
                    for dy in range(start[1] - target[1]):
                        self.status[start[0]][start[1] - dy] = marker[0]
            elif start[1] == target[1]:
                if target[0] >= start[0]:
                    for dx in range(target[0] - start[0] + 1):
                        self.status[start[0] + dx][start[1]] = marker[0]
                else:
                    for dx in range(start[0] - target[0]):
                        self.status[start[0] - dx][start[1]] = marker[0]
            else:
                raise ValueError
            start = target
        for i in range(self.height):
            wall_counter = 0
            max_wall = self.status[i].count(marker[0])
            for j in range(self.width):
                if self.status[i][j] == marker[0]:
                    wall_counter += 1
                    if wall_counter == max_wall:
                        break
                else:
                    if self.status[i][j] != marker[0] and wall_counter % 2 == 1:
                        self.status[i][j] = marker[1]


class CellError(Exception):
    pass
