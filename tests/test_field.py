# BUG: 終点を追加すると色々不便
import pytest
from judge.field import Field, CellError


@pytest.fixture
def field():
    return Field((12, 12), "teamA", "teamB")


@pytest.fixture
def plane_status():
    return [["*" for j in range(12)] for i in range(12)]


@pytest.fixture
def tops():
    return [(0, 0), (0, 2), (2, 2), (2, 0), (0, 0)]


@pytest.fixture
def tops6():
    return [(0, 0), (0, 3), (2, 3), (2, 2), (3, 2), (3, 0), (0, 0)]


@pytest.fixture
def tops8():
    return [(1, 1), (1, 7), (5, 7), (5, 5), (3, 5), (3, 3), (6, 3), (6, 1), (1, 1)]


def test_init_base_point(field):
    for line in field.base_point:
        for value in line:
            assert -16 <= value <= 16
            assert isinstance(value, int)


def test_init_status(field):
    for line in field.status:
        for st in line:
            assert st == "*"


def test_init_calc_point(field):
    for v in field.calc_point().values():
        assert v == 0


def test_build_castle_1(field, plane_status, tops):
    field.build_castle("O", tops)

    for i in range(3):
        for j in range(3):
            if i == 1 and j == 1:
                pass
            else:
                plane_status[i][j] = "O"
    assert field.status == plane_status


def test_build_castle_2(field):
    with pytest.raises(ValueError):
        field.build_castle("O", [(0, 0), (2, 4), (0, 4), (4, 0), (0, 0)])


def test_build_castle_3(field):
    with pytest.raises(ValueError):
        field.build_castle("O", [(0, 0), (0, 2), (0, 0)])


def test_build_castle_4(field):
    with pytest.raises(ValueError):
        field.build_castle("O", [(0, 0), (0, 2), (2, 2), (0, 0)])


def test_build_castle_5(field, plane_status, tops6):
    field.build_castle("O", tops6)
    # 人力
    plane_status[0][0] = "O"
    plane_status[0][1] = "O"
    plane_status[0][2] = "O"
    plane_status[0][3] = "O"
    plane_status[1][0] = "O"
    plane_status[1][3] = "O"
    plane_status[2][0] = "O"
    plane_status[2][2] = "O"
    plane_status[2][3] = "O"
    plane_status[3][0] = "O"
    plane_status[3][1] = "O"
    plane_status[3][2] = "O"
    assert field.status == plane_status


def test_fill_1(field, plane_status, tops):
    field.build_castle("O", tops)
    field.fill("O", "+", tops)

    for i in range(3):
        for j in range(3):
            if i == 1 and j == 1:
                plane_status[i][j] = "+"
            else:
                plane_status[i][j] = "O"
    assert field.status == plane_status


def test_fill_2(field):
    uncorrect_tops = [(0, 0), (0, 2), (2, 3), (2, 0), (0, 0)]
    with pytest.raises(ValueError):
        field.fill("O", "+", uncorrect_tops)


def test_fill_3(field, plane_status, tops):
    sub_tops = [(0, 3), (0, 5), (2, 5), (2, 3), (0, 3)]
    field.build_castle("O", tops)
    field.build_castle("O", sub_tops)
    field.fill("O", "+", tops)
    field.fill("O", "+", sub_tops)

    for i in range(3):
        for j in range(3):
            if i == 1 and j == 1:
                plane_status[i][j] = "+"
                plane_status[i][j + 3] = "+"
            else:
                plane_status[i][j] = "O"
                plane_status[i][j + 3] = "O"
    assert field.status == plane_status


def test_calc_point_1(field, tops):
    field.build_castle("O", tops)
    field.fill("O", "+", tops)
    Xtops = [(0, 3), (0, 5), (2, 5), (2, 3), (0, 3)]
    field.build_castle("X", Xtops)
    field.fill("X", "-", Xtops)

    point_a, point_b = 0, 0
    for i in range(3):
        for j in range(3):
            if i == 1 and j == 1:
                point_a += abs(field.base_point[i][j])
                point_b += abs(field.base_point[i][j + 3])

            else:
                point_a += field.base_point[i][j]
                point_b += field.base_point[i][j + 3]

    point = field.calc_point()
    assert point["teamA"] == point_a
    assert point["teamB"] == point_b


def test_calc_point_2(field):
    field.status[-1][-1] = "Q"
    with pytest.raises(CellError):
        field.calc_point()


def same_path(path_a, path_b):
    return (path_a == path_b) or (path_a[::-1] == path_b)


def reduction(path: tuple):
    def calc_diff(before: tuple, after: tuple):
        return (after[0] - before[0], after[1] - before[1])

    if not path:
        return []
    reducted_path = []
    before_diff = calc_diff(path[-2], path[-1])
    for i in range(len(path) - 1):
        diff = calc_diff(path[i % len(path)], path[(i + 1) % len(path)])
        if diff != before_diff:
            reducted_path.append(path[i])
        before_diff = diff
    return reducted_path


def test_judge_castle_1(field):
    castles = field.judge_castle()
    assert not(castles)


def test_judge_castle_2(field, tops):
    field.build_castle("O", tops)
    castles = field.judge_castle()
    assert len(castles) == 1
    assert same_path(sorted(reduction(castles[0])), sorted(set(tops)))


def test_judge_zone_1(field, tops):
    field.build_castle("O", tops)
    zones = field.judge_zone("O")
    assert zones == [(1, 1), ]


def test_judge_zone_2(field, tops6):
    field.build_castle("O", tops6)
    zones = field.judge_zone("O")
    assert zones == [(1, 1), (1, 2), (2, 1)]


def test_judge_zone_3(field, tops8):
    field.build_castle("O", tops8)
    zones = field.judge_zone("O")
    assert zones == [(2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (3, 2), (3, 6), (4, 2), (4, 6), (5, 2)]


def test_update(field, plane_status, tops):
    field.build_castle("O", tops)
    field.update()
    for i in range(3):
        for j in range(3):
            if i == j == 1:
                plane_status[i][j] = "+"
            else:
                plane_status[i][j] = "O"
    assert field.status == plane_status
