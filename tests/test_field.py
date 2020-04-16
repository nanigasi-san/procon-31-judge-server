import pytest
from judge.field import Field, CellError


@pytest.fixture
def field():
    return Field((12, 12), "teamA", "teamB")


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


def test_fill_1(field):
    field.fill(("O", "+"), ((0, 0), (0, 2), (2, 2), (2, 0), (0, 0)))
    res = [["*" for j in range(12)] for i in range(12)]
    for i in range(3):
        for j in range(3):
            if i == 1 and j == 1:
                res[i][j] = "+"
            else:
                res[i][j] = "O"
    assert field.status == res


def test_fill_2(field):
    with pytest.raises(ValueError):
        field.fill(("O", "+"), ((0, 0), (2, 2), (2, 0), (0, 0)))


def test_calc_point_1(field):
    field.fill(("O", "+"), ((0, 0), (0, 2), (2, 2), (2, 0), (0, 0)))
    field.fill(("X", "-"), ((0, 3), (0, 5), (2, 5), (2, 3), (0, 3)))

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
