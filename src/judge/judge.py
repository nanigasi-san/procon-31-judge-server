from .field import Field, Point, Grid
from collections import deque, defaultdict
from typing import List, Dict, Tuple, Set, Deque, DefaultDict


class Judge:
    def __init__(self, field: Field, teams: Tuple[str, str]):
        self.field = field
        self.teams = teams
        self.wall_mark = {teams[0]: "O", teams[1]: "X"}
        self.zone_mark = {teams[0]: "+", teams[1]: "-"}

    def calc_point(self) -> Dict[str, int]:
        team_point: Dict[str, int] = {team: 0 for team in self.teams}
        for point in Point.gen_all_points(*self.field.size):
            cell = self.field.status.at(point)
            if cell == "*":
                pass
            elif cell == "O":
                team_point[self.teams[0]] += self.field.base_point.at(point)
            elif cell == "+":
                team_point[self.teams[0]] += abs(self.field.base_point.at(point))
            elif cell == "X":
                team_point[self.teams[1]] += self.field.base_point.at(point)
            elif cell == "-":
                team_point[self.teams[1]] += abs(self.field.base_point.at(point))
            else:
                raise CellError("this cell{0} has \"{1}\". It is not supposed field.status.".format(point, cell))

        return team_point

    def build_castle(self, wall: str, tops: List[Point]) -> None:
        # 城郭の最小構成は正方形なので、頂点が4つ未満なら不正
        if len(tops) < 4:
            raise ValueError("The castle must pass only once beyond the starting point and consist only of straight lines parallel to the x or y axis. {0} is an invalid entry.".format(tops))
        start = tops[0]
        tops = tops[:] + [start]
        for i in range(1, len(tops)):
            target = tops[i]
            if start.x == target.x:
                if target.y >= start.y:
                    for dy in range(target.y - start.y + 1):
                        self.field.status[start.x][start.y + dy] = wall
                else:
                    for dy in range(start.y - target.y):
                        self.field.status[start.x][start.y - dy] = wall
            elif start.y == target.y:
                if target.x >= start.x:
                    for dx in range(target.x - start.x + 1):
                        self.field.status[start.x + dx][start.y] = wall
                else:
                    for dx in range(start.x - target.x):
                        self.field.status[start.x - dx][start.y] = wall
            else:
                raise ValueError("tops must be identical in x or y in each of its neighbors. (e.g., (0, 0)->(0, 3), (3, 5) -> (1, 5)).\n{0} -> {1} is not correct.".format(start, target))
            start = target

    def fill(self, wall: str, zone: str, tops: List[Point]) -> None:
        # validation
        for i in range(len(tops) - 1):
            if tops[i].x != tops[i + 1].x and tops[i].y != tops[i + 1].y:
                raise ValueError("tops must be identical in x or y in each of its neighbors. (e.g., (0, 0)->(0, 3), (3, 5) -> (1, 5)).\n{0} -> {1} is not correct.".format(tops[i], tops[i + 1]))

        if len(tops) == 4:  # 長方形
            tops = tops[:] + [tops[0]]
            xlist, ylist = [tops[i].x for i in range(len(tops))], [tops[i].y for i in range(len(tops))]
            mnx, mxx = min(xlist), max(xlist)
            mny, mxy = min(ylist), max(ylist)
            for x in range(mnx + 1, mxx):
                for y in range(mny + 1, mxy):
                    self.field.status[x][y] = zone

    def judge_castle(self) -> Dict[str, List[List[Point]]]:
        def dfs_gird(graph: Grid[str], wall: str, start: Point, x_lim: int, y_lim: int) -> Dict[Point, Point]:
            seen: Set[Point] = {start}
            todo: Deque[Point] = deque([start])
            prev: Dict[Point, Point] = {}  # 経路復元
            one_steps = ((1, 0), (-1, 0), (0, 1), (0, -1))
            while todo:
                now = todo.pop()
                for dxy in one_steps:
                    target = now.update(dxy)
                    if not ((0 <= target.x < x_lim) and (0 <= target.y < y_lim)):
                        continue
                    if graph.at(target) == wall:
                        try:
                            if prev[now] == target:
                                continue
                        except KeyError:
                            pass
                        prev[target] = now
                        if target not in seen:
                            todo.append(target)
                            seen.add(target)
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

        res: Dict[str, List[List[Point]]] = {team: [] for team in self.teams}
        seen: List[List[Point]] = []
        for team in self.teams:
            for start in Point.gen_all_points(*self.field.size):
                prev = dfs_gird(self.field.status, self.wall_mark[team], start, *self.field.size)
                path = restore_path(start, prev)
                expanded_path = sorted(set(path))
                if path and expanded_path not in seen:
                    res[team].append(path)
                seen.append(expanded_path)
        return res

    def judge_zone(self) -> Dict[str, Set[Point]]:
        castles = self.judge_castle()

        def sfs_grid(graph: Grid[str], wall: str, start: Point, x_lim: int, y_lim: int) -> List[List[Point]]:
            res: List[List[Point]] = [[] for _ in range(4)]
            one_steps = ((1, 0), (-1, 0), (0, 1), (0, -1))
            if graph.at(start) in self.wall_mark.values():  # 城壁だった時
                return []
            for dxy, path in zip(one_steps, res):
                target = start.update(dxy)
                while (0 <= target.x < x_lim) and (0 <= target.y < y_lim):
                    if graph.at(target) == wall:
                        path.append(target)
                    target = target.update(dxy)
            return res

        def check_union(points_4: List[List[Point]], castle: List[Point]) -> bool:
            if not points_4:
                raise ValueError("takes empty list")

            def common_walls(points: List[Point]) -> Set[Point]:
                return set(points) & set(castle)

            return all(map(common_walls, points_4))

        zones: DefaultDict[str, Set[Point]] = defaultdict(set)
        parent_castle: Dict[Point, Tuple[str, List[Point]]] = {}
        for point in Point.gen_all_points(*self.field.size):
            for team in self.teams:
                p = sfs_grid(self.field.status, self.wall_mark[team], point, *self.field.size)
                for castle in castles[team]:
                    if p and check_union(p, castle):
                        if (point in parent_castle.keys()):
                            if (len(parent_castle[point][1]) > len(castle)):
                                zones[parent_castle[point][0]].remove(point)
                                zones[team].add(point)
                                parent_castle[point] = (team, castle)
                        else:
                            parent_castle[point] = (team, castle)
                            zones[team].add(point)
        return zones

    def update(self) -> None:
        for team in self.teams:
            for point in self.judge_zone()[team]:
                self.field.status[point.x][point.y] = self.zone_mark[team]


class CellError(Exception):
    pass
