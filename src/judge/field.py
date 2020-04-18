from random import randint
from collections import deque
from typing import List, Dict, Tuple, Deque

Point = Tuple[int, int]


class Field:
    def __init__(self, size: Point, *team: str):
        self.height, self.width = size
        self.base_point = [[randint(-16, 16) for _ in range(self.width)] for _ in range(self.height)]
        self.status = [["*" for _ in range(self.width)] for _ in range(self.height)]
        self.team = team

    def calc_point(self) -> Dict[str, int]:
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

    def build_castle(self, wall: str, tops: List[Point]) -> None:
        # 城郭の最小構成は正方形なので、頂点が5つ以下なら不正
        if len(tops) < 5:
            raise ValueError("The castle must pass only once beyond the starting point and consist only of straight lines parallel to the x or y axis. {0} is an invalid entry.".format(tops))
        start = tops[0]
        for i in range(1, len(tops)):
            target = tops[i]
            if start[0] == target[0]:
                if target[1] >= start[1]:
                    for dy in range(target[1] - start[1] + 1):
                        self.status[start[0]][start[1] + dy] = wall
                else:
                    for dy in range(start[1] - target[1]):
                        self.status[start[0]][start[1] - dy] = wall
            elif start[1] == target[1]:
                if target[0] >= start[0]:
                    for dx in range(target[0] - start[0] + 1):
                        self.status[start[0] + dx][start[1]] = wall
                else:
                    for dx in range(start[0] - target[0]):
                        self.status[start[0] - dx][start[1]] = wall
            else:
                raise ValueError("tops must be identical in x or y in each of its neighbors. (e.g., (0, 0)->(0, 3), (3, 5) -> (1, 5)).\n{0} -> {1} is not correct.".format(start, target))
            start = target

    def fill(self, wall: str, zone: str, tops: List[Point]) -> None:
        # validation
        for i in range(len(tops) - 1):
            if tops[i][0] != tops[i + 1][0] and tops[i][1] != tops[i + 1][1]:
                raise ValueError("tops must be identical in x or y in each of its neighbors. (e.g., (0, 0)->(0, 3), (3, 5) -> (1, 5)).\n{0} -> {1} is not correct.".format(tops[i], tops[i + 1]))

        # TODO: 5頂点以上の城郭判定
        if len(tops) == 5:  # 長方形
            xlist, ylist = [tops[i][0] for i in range(len(tops))], [tops[i][1] for i in range(len(tops))]
            mnx, mxx = min(xlist), max(xlist)
            mny, mxy = min(ylist), max(ylist)
            for x in range(mnx + 1, mxx):
                for y in range(mny + 1, mxy):
                    self.status[x][y] = zone
            return

    # TODO: 何も返さずメンバを更新するようにする
    def judge_castle(self) -> List[List[Point]]:
        def dfs_gird(graph: List[List[str]], start: Point, x_lim: int, y_lim: int) -> Dict[Point, Point]:
            seen = {start}
            todo: Deque[Point] = deque()
            todo.append(start)
            prev: Dict[Point, Point] = {}  # 経路復元
            one_steps = ((1, 0), (-1, 0), (0, 1), (0, -1))
            while todo:
                x, y = todo.pop()
                for dx, dy in one_steps:
                    nx, ny = x + dx, y + dy
                    if not ((0 <= nx < x_lim) and (0 <= ny < y_lim)):
                        continue
                    nxy = (nx, ny)
                    if graph[nx][ny] == "O":
                        try:
                            if prev[(x, y)] == nxy:
                                continue
                        except KeyError:
                            pass
                        prev[nxy] = (x, y)
                        if nxy not in seen:
                            todo.append(nxy)
                            seen.add(nxy)
            return prev

        def restore_path(start: Point, prev: Dict[Point, Point]) -> List[Point]:
            path = [start]
            while True:
                try:
                    path.append(prev[path[-1]])
                    if path[-1] == start:
                        return path
                except KeyError:
                    return []

        res = []
        seen: List[List[Point]] = []
        for i in range(self.height):
            for j in range(self.width):
                start = (i, j)
                prev = dfs_gird(self.status, start, self.height, self.height)
                path = restore_path(start, prev)
                if path and (sorted(set(path)) not in seen):
                    res.append(path)
                seen.append(sorted(set(path)))
        return res

    def judge_zone(self, wall: str) -> List[Point]:
        castle = self.judge_castle()[0]

        def sfs(graph: List[List[str]], start: Point, x_lim: int, y_lim: int) -> List[List[Point]]:
            res: List[List[Point]] = [[] for _ in range(4)]
            one_steps = ((1, 0), (-1, 0), (0, 1), (0, -1))
            for i in range(4):
                x, y = start
                if graph[x][y] == "O":
                    break
                dx, dy = one_steps[i]
                while (0 <= x + dx < x_lim) and (0 <= y + dy < y_lim):
                    x += dx
                    y += dy
                    if graph[x][y] == "O":
                        res[i].append((x, y))
            return res

        def check_union(points: List[List[Point]], castle: List[Point]) -> bool:
            for a in points[0]:
                for b in points[1]:
                    for c in points[2]:
                        for d in points[3]:
                            if (a in castle) and (b in castle) and (c in castle) and (d in castle):
                                return True
            return False
        zones = []
        for x in range(self.height):
            for y in range(self.width):
                p = sfs(self.status, (x, y), self.height, self.width)
                if check_union(p, castle):
                    zones.append((x, y))
        return zones

    def update(self) -> None:
        for x, y in self.judge_zone("O"):
            self.status[x][y] = "+"
        return


class CellError(Exception):
    pass
