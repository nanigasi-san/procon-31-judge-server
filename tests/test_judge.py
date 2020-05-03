import pytest
from judge.field import Point
from judge.judge import Path, Judge, CellError
from judge.agent import Agent


def convert_point(tops):
    def _point(tops):
        return Point(*tops)
    return list(map(_point, tops))


@pytest.fixture
def path():
    return Path([Point(0, 0), Point(0, 4), Point(3, 4), Point(3, 0)])


@pytest.fixture
def judge(field):
    return Judge(field, ("teamA", "teamB"))


@pytest.fixture
def mock_status():
    return [["*" for j in range(12)] for i in range(12)]


@pytest.fixture
def tops4_1():
    return convert_point([(0, 0), (0, 2), (2, 2), (2, 0)])


@pytest.fixture
def tops4_2():
    return convert_point([(0, 3), (0, 5), (2, 5), (2, 3)])


@pytest.fixture
def tops4_3():
    return convert_point([(0, 0), (0, 7), (7, 7), (7, 0)])


@pytest.fixture
def tops4_4():
    return convert_point([(2, 2), (2, 5), (5, 5), (5, 2)])


@pytest.fixture
def tops6():
    return convert_point([(0, 0), (0, 3), (2, 3), (2, 2), (3, 2), (3, 0)])


@pytest.fixture
def tops8():
    return convert_point([(1, 1), (1, 7), (5, 7), (5, 5), (3, 5), (3, 3), (6, 3), (6, 1)])


def test_path_reduction_empty_1():
    path = Path([])
    assert not path.reduction()


def test_path_reduction_empty_2():
    path = Path()
    assert not path.reduction()


def test_path_eq_1(path):
    assert not path == tuple(path)


def test_path_eq_2(path):
    assert not path == path[:-1]


def test_path_eq_3(path):
    assert not path == Path([Point(0, 0), Point(2, 0), Point(2, 4), Point(0, 4)])


def test_init_judge(judge, field):
    assert judge.field == field


def test_init_teams(judge):
    assert judge.teams[0] == "teamA"
    assert judge.teams[1] == "teamB"


def test_init_gen_agent(judge):
    for team in judge.teams:
        for agent in judge.agents[team]:
            assert isinstance(agent, Agent)


def test_build_castle_1(judge, mock_status, tops4_1):
    judge.build_castle("O", tops4_1)

    for i in range(3):
        for j in range(3):
            if i == 1 and j == 1:
                pass
            else:
                mock_status[i][j] = "O"
    assert judge.field.status == mock_status


def test_build_castle_2(judge):
    with pytest.raises(ValueError):
        judge.build_castle("O", convert_point([(0, 0), (2, 4), (0, 4), (4, 0)]))


def test_build_castle_3(judge):
    with pytest.raises(ValueError):
        judge.build_castle("O", convert_point([(0, 0), (0, 2)]))


def test_build_castle_4(judge):
    with pytest.raises(ValueError):
        judge.build_castle("O", convert_point([(0, 0), (0, 2), (2, 2)]))


def test_build_castle_5(judge, mock_status, tops6):
    judge.build_castle("O", tops6)
    # 人力
    mock_status[0][0] = "O"
    mock_status[0][1] = "O"
    mock_status[0][2] = "O"
    mock_status[0][3] = "O"
    mock_status[1][0] = "O"
    mock_status[1][3] = "O"
    mock_status[2][0] = "O"
    mock_status[2][2] = "O"
    mock_status[2][3] = "O"
    mock_status[3][0] = "O"
    mock_status[3][1] = "O"
    mock_status[3][2] = "O"
    assert judge.field.status == mock_status


def test_fill_1(judge, mock_status, tops4_1):
    judge.build_castle("O", tops4_1)
    judge.fill("O", "+", tops4_1)

    for i in range(3):
        for j in range(3):
            if i == 1 and j == 1:
                mock_status[i][j] = "+"
            else:
                mock_status[i][j] = "O"
    assert judge.field.status == mock_status


def test_fill_2(judge):
    uncorrect_tops = convert_point([(0, 0), (0, 2), (2, 3), (2, 0)])
    with pytest.raises(ValueError):
        judge.fill("O", "+", uncorrect_tops)


def test_fill_3(judge, mock_status, tops4_1):
    sub_tops = convert_point([(0, 3), (0, 5), (2, 5), (2, 3)])
    judge.build_castle("O", tops4_1)
    judge.build_castle("O", sub_tops)
    judge.fill("O", "+", tops4_1)
    judge.fill("O", "+", sub_tops)

    for i in range(3):
        for j in range(3):
            if i == 1 and j == 1:
                mock_status[i][j] = "+"
                mock_status[i][j + 3] = "+"
            else:
                mock_status[i][j] = "O"
                mock_status[i][j + 3] = "O"
    assert judge.field.status == mock_status


def test_calc_point_1(judge, tops4_1):
    judge.build_castle("O", tops4_1)
    judge.fill("O", "+", tops4_1)
    Xtops = convert_point([(0, 3), (0, 5), (2, 5), (2, 3)])
    judge.build_castle("X", Xtops)
    judge.fill("X", "-", Xtops)

    point_a, point_b = 0, 0
    for i in range(3):
        for j in range(3):
            if i == 1 and j == 1:
                point_a += abs(judge.field.base_point[i][j])
                point_b += abs(judge.field.base_point[i][j + 3])

            else:
                point_a += judge.field.base_point[i][j]
                point_b += judge.field.base_point[i][j + 3]

    point = judge.calc_point()
    assert point["teamA"] == point_a
    assert point["teamB"] == point_b


def test_calc_point_2(judge):
    judge.field.status[-1][-1] = "Q"
    with pytest.raises(CellError):
        judge.calc_point()


def test_judge_castle_1(judge):
    castles = judge.judge_castle()
    assert not(castles["teamA"])
    assert not(castles["teamB"])


def test_judge_castle_2(judge, tops4_1):
    judge.build_castle("O", tops4_1)
    castles = judge.judge_castle()
    assert len(castles["teamA"]) == 1
    assert not(castles["teamB"])
    assert castles["teamA"][0].reduction() == tops4_1


def test_judge_castle_3(judge, tops4_2):
    judge.build_castle("X", tops4_2)
    castles = judge.judge_castle()
    assert not(castles["teamA"])
    assert len(castles["teamB"]) == 1
    assert castles["teamB"][0].reduction() == tops4_2


def test_judge_castle_4(judge, tops4_1, tops4_2):
    judge.build_castle("O", tops4_1)
    judge.build_castle("X", tops4_2)
    castles = judge.judge_castle()
    assert len(castles["teamA"]) == 1
    assert len(castles["teamB"]) == 1
    assert castles["teamA"][0].reduction() == tops4_1
    assert castles["teamB"][0].reduction() == tops4_2


def test_judge_castle_5(judge, tops4_3, tops4_4):
    judge.build_castle("O", tops4_3)
    judge.build_castle("X", tops4_4)
    castles = judge.judge_castle()
    assert len(castles["teamA"]) == 1
    assert len(castles["teamB"]) == 1
    assert castles["teamA"][0].reduction() == tops4_3
    assert castles["teamB"][0].reduction() == tops4_4


def test_judge_castle_6(judge, tops4_3, tops4_4):
    judge.build_castle("X", tops4_3)
    judge.build_castle("O", tops4_4)
    castles = judge.judge_castle()
    assert len(castles["teamA"]) == 1
    assert len(castles["teamB"]) == 1
    assert castles["teamB"][0].reduction() == tops4_3
    assert castles["teamA"][0].reduction() == tops4_4


def test_judge_zone_1(judge, tops4_1):
    judge.build_castle("O", tops4_1)
    zones = judge.judge_zone()
    assert zones["teamA"] == {(1, 1), }


def test_judge_zone_2(judge, tops6):
    judge.build_castle("O", tops6)
    zones = judge.judge_zone()
    assert zones["teamA"] == {(1, 1), (1, 2), (2, 1)}


def test_judge_zone_3(judge, tops8):
    judge.build_castle("O", tops8)
    zones = judge.judge_zone()
    assert zones["teamA"] == {(2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (3, 2), (3, 6), (4, 2), (4, 6), (5, 2)}


def test_judge_zone_4(judge, tops4_2):
    judge.build_castle("X", tops4_2)
    zones = judge.judge_zone()
    assert not(zones["teamA"])
    assert len(zones["teamB"]) == 1
    assert zones["teamB"] == {(1, 4), }


def test_judge_zone_5(judge, tops4_1, tops4_2):
    judge.build_castle("O", tops4_1)
    judge.build_castle("X", tops4_2)
    zones = judge.judge_zone()
    assert len(zones["teamA"]) == 1
    assert len(zones["teamB"]) == 1
    assert zones["teamA"] == {(1, 1), }
    assert zones["teamB"] == {(1, 4), }


def test_judge_zone_6(judge, tops4_3, tops4_4):
    judge.build_castle("O", tops4_3)
    judge.build_castle("X", tops4_4)
    zones = judge.judge_zone()
    assert len(zones["teamA"]) == 20
    assert len(zones["teamB"]) == 4
    assert zones["teamA"] == {(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (2, 1), (2, 6), (3, 1), (3, 6), (4, 1), (4, 6), (5, 1), (5, 6), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6)}
    assert zones["teamB"] == {(3, 3), (3, 4), (4, 3), (4, 4)}


def test_judge_zone_7(judge, tops4_3, tops4_4):
    judge.build_castle("O", tops4_4)
    judge.build_castle("X", tops4_3)
    zones = judge.judge_zone()
    assert len(zones["teamA"]) == 4
    assert len(zones["teamB"]) == 20
    assert zones["teamA"] == {(3, 3), (3, 4), (4, 3), (4, 4)}
    assert zones["teamB"] == {(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (2, 1), (2, 6), (3, 1), (3, 6), (4, 1), (4, 6), (5, 1), (5, 6), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6)}


def test_update_1(judge, mock_status, tops4_1):
    judge.build_castle("O", tops4_1)
    judge.update()
    for i in range(3):
        for j in range(3):
            if i == j == 1:
                mock_status[i][j] = "+"
            else:
                mock_status[i][j] = "O"
    assert judge.field.status == mock_status


def test_update_2(judge, mock_status, tops4_1, tops4_2):
    judge.build_castle("O", tops4_1)
    judge.build_castle("X", tops4_2)
    judge.update()
    for i in range(3):
        for j in range(3):
            if i == j == 1:
                mock_status[i][j] = "+"
                mock_status[i][j + 3] = "-"
            else:
                mock_status[i][j] = "O"
                mock_status[i][j + 3] = "X"
    assert judge.field.status == mock_status


def test_submit_agents_activity_placement_1(judge):
    temp_grid = judge.submit_agents_activity("./tests/datas/agent/placement/data1.json")
    for point in Point.gen_all_points(2, 6):
        assert temp_grid.at(point) == 1


def test_submit_agents_activity_placement_2(judge):
    temp_grid = judge.submit_agents_activity("./tests/datas/agent/placement/data2.json")
    for point in Point.gen_all_points(2, 6):
        if point == Point(0, 0):
            assert temp_grid.at(point) == 0
        else:
            assert temp_grid.at(point) == 1


def test_submit_agents_activity_placement_3(judge):
    temp_agent = judge.agents["teamA"][0]
    temp_agent.on_field = True
    temp_agent.point = Point(0, 0)

    temp_grid = judge.submit_agents_activity("./tests/datas/agent/placement/data3.json")
    for point in Point.gen_all_points(2, 6):
        assert temp_grid.at(point) == 1


def test_submit_agents_activity_placement_4(judge):
    judge.field.status[0][0] = "X"

    temp_grid = judge.submit_agents_activity("./tests/datas/agent/placement/data4.json")
    for point in Point.gen_all_points(2, 6):
        if point == Point(0, 0):
            assert temp_grid.at(point) == 0
        else:
            assert temp_grid.at(point) == 1


def test_submit_agents_activity_placement_5(judge):
    temp_grid = judge.submit_agents_activity("./tests/datas/agent/placement/data5.json")
    for point in Point.gen_all_points(2, 6):
        if point == Point(0, 0):
            assert temp_grid.at(point) == 0
        else:
            assert temp_grid.at(point) == 1


def test_submit_agents_activity_move_1(judge):
    temp_agent = judge.agents["teamA"][0]
    temp_agent.on_field = True
    temp_agent.point = Point(0, 0)

    temp_grid = judge.submit_agents_activity("./tests/datas/agent/move/data1.json")
    for point in Point.gen_all_points(2, 6):
        if point == Point(0, 0):
            assert temp_grid.at(point) == 0
        elif point == Point(1, 0):
            assert temp_grid.at(point) == 2
        else:
            assert temp_grid.at(point) == 1


def test_submit_agents_activity_move_2(judge):
    temp_grid = judge.submit_agents_activity("./tests/datas/agent/move/data2.json")
    for point in Point.gen_all_points(2, 6):
        if point == Point(0, 0):
            assert temp_grid.at(point) == 0
        else:
            assert temp_grid.at(point) == 1


def test_submit_agents_activity_move_3(judge):
    temp_agent = judge.agents["teamA"][0]
    temp_agent.on_field = True
    temp_agent.point = Point(0, 0)

    temp_grid = judge.submit_agents_activity("./tests/datas/agent/move/data3.json")
    for point in Point.gen_all_points(2, 6):
        assert temp_grid.at(point) == 1


def test_submit_agents_activity_move_4(judge):
    judge.field.status[0][6] = "X"
    temp_agent = judge.agents["teamA"][5]
    temp_agent.on_field = True
    temp_agent.point = Point(0, 5)

    temp_grid = judge.submit_agents_activity("./tests/datas/agent/move/data4.json")
    for point in Point.gen_all_points(2, 7):
        if point.y == 6:
            assert temp_grid.at(point) == 0
        else:
            assert temp_grid.at(point) == 1


def test_submit_agents_activity_remove_1(judge):
    temp_agent = judge.agents["teamA"][0]
    temp_agent.on_field = True
    temp_agent.point = Point(0, 0)
    judge.field.status[1][0] = "X"

    temp_grid = judge.submit_agents_activity("./tests/datas/agent/remove/data1.json")
    assert temp_grid.at(Point(0, 0)) == 1
    assert temp_grid.at(Point(1, 0)) == 1


def test_submit_agents_activity_remove_2(judge):
    temp_grid = judge.submit_agents_activity("./tests/datas/agent/remove/data2.json")
    assert temp_grid.at(Point(0, 0)) == 0


def test_submit_agents_activity_remove_3(judge):
    temp_agent = judge.agents["teamA"][0]
    temp_agent.on_field = True
    temp_agent.point = Point(0, 0)

    temp_grid = judge.submit_agents_activity("./tests/datas/agent/remove/data3.json")
    assert temp_grid[-1][0] == 0
    assert temp_grid.at(Point(0, 0)) == 1


def test_submit_agents_activity_remove_4(judge):
    temp_agent = judge.agents["teamA"][0]
    temp_agent.on_field = True
    temp_agent.point = Point(0, 0)

    temp_grid = judge.submit_agents_activity("./tests/datas/agent/remove/data4.json")
    assert temp_grid.at(Point(0, 0)) == 1
    assert temp_grid.at(Point(1, 0)) == 0


def test_submit_agents_activity_other_1(judge):
    temp_agent = judge.agents["teamA"][0]
    temp_agent.on_field = True
    temp_agent.point = Point(0, 0)
    temp_grid = judge.submit_agents_activity("./tests/datas/agent/other/data1.json")
    for point in Point.gen_all_points(2, 6):
        assert temp_grid.at(point) == 1


def test_submit_agents_activity_other_2(judge):
    temp_agent = judge.agents["teamA"][0]
    temp_agent.on_field = True
    temp_agent.point = Point(0, 0)
    temp_grid = judge.submit_agents_activity("./tests/datas/agent/other/data2.json")
    for point in Point.gen_all_points(2, 6):
        assert temp_grid.at(point) == 1


def test_submit_agents_activity_missing_agent_1(judge):
    temp_grid = judge.submit_agents_activity("./tests/datas/agent/missing_agent/data1.json")
    assert not judge.agents["teamA"][5].on_field
    for point in Point.gen_all_points(2, 6):
        if point == Point(0, 5):
            assert temp_grid.at(point) == 0
        else:
            assert temp_grid.at(point) == 1


def test_submit_agents_activity_missing_agent_2(judge):
    temp_agent = judge.agents["teamA"][5]
    temp_agent.on_field = True
    temp_agent.point = Point(0, 5)
    temp_grid = judge.submit_agents_activity("./tests/datas/agent/missing_agent/data2.json")
    for point in Point.gen_all_points(2, 6):
        assert temp_grid.at(point) == 1
