import pytest
from judge.field import Point, Grid


@pytest.fixture
def point():
    return Point(0, 0)


@pytest.fixture
def graph():
    N = 29  # 適当です
    return Grid([["*" for _ in range(N)] for _ in range(N)])


def test_point_init(point):
    assert point.x == 0
    assert point.y == 0


def test_point_immutable_1(point):
    with pytest.raises(AttributeError):
        point.x = 1


def test_point_immutable_2(point):
    with pytest.raises(AttributeError):
        point.y = 1


def test_point_add(point):
    assert point.add((1, 1)) == (1, 1)


def test_point_gen_all_points():
    assert set(Point.gen_all_points(2, 3)) == {(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)}


def test_graph_init(graph):
    for line in graph:
        for ele in line:
            assert ele == "*"


def test_graph_at(graph):
    graph[0][0] = "O"
    graph[-1][-1] = "X"
    graph[1][1] = "+"
    graph[-2][-2] = "-"
    assert graph.at((Point(0, 0))) == "O"
    assert graph.at((Point(-1, -1))) == "X"
    assert graph.at((Point(1, 1))) == "+"
    assert graph.at((Point(-2, -2))) == "-"


def test_field_init_size(field):
    assert field.size == (12, 12)
    assert field.height == 12
    assert field.width == 12


def test_field_init_base_point(field):
    for line in field.base_point:
        for ele in line:
            assert -16 <= ele <= 16
            assert isinstance(ele, int)


def test_field_init_status(field):
    for line in field.status:
        for ele in line:
            assert ele == "*"
