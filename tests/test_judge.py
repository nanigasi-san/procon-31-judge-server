import pytest
from judge import Judge, CellError


@pytest.fixture
def judge(field):
    return Judge(field, ("teamA", "teamB"))


@pytest.fixture
def mock_status():
    return [["*" for j in range(12)] for i in range(12)]


@pytest.fixture
def tops4_1():
    return [(0, 0), (0, 2), (2, 2), (2, 0)]


@pytest.fixture
def tops4_2():
    return [(0, 3), (0, 5), (2, 5), (2, 3)]


@pytest.fixture
def tops6():
    return [(0, 0), (0, 3), (2, 3), (2, 2), (3, 2), (3, 0)]


@pytest.fixture
def tops8():
    return [(1, 1), (1, 7), (5, 7), (5, 5), (3, 5), (3, 3), (6, 3), (6, 1)]


def test_init_judge(judge, field):
    assert judge.field == field


def test_init_teams(judge):
    assert judge.teams[0] == "teamA"
    assert judge.teams[1] == "teamB"


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
        judge.build_castle("O", [(0, 0), (2, 4), (0, 4), (4, 0)])


def test_build_castle_3(judge):
    with pytest.raises(ValueError):
        judge.build_castle("O", [(0, 0), (0, 2)])


def test_build_castle_4(judge):
    with pytest.raises(ValueError):
        judge.build_castle("O", [(0, 0), (0, 2), (2, 2)])


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
    uncorrect_tops = [(0, 0), (0, 2), (2, 3), (2, 0)]
    with pytest.raises(ValueError):
        judge.fill("O", "+", uncorrect_tops)


def test_fill_3(judge, mock_status, tops4_1):
    sub_tops = [(0, 3), (0, 5), (2, 5), (2, 3)]
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
    Xtops = [(0, 3), (0, 5), (2, 5), (2, 3)]
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


# TODO: ここらへん別にまとめる
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


def test_judge_castle_1(judge):
    castles = judge.judge_castle()
    assert not(castles["teamA"])
    assert not(castles["teamB"])


def test_judge_castle_2(judge, tops4_1):
    judge.build_castle("O", tops4_1)
    castles = judge.judge_castle()
    assert len(castles["teamA"]) == 1
    assert not(castles["teamB"])
    # TODO: ここのはんていもっと綺麗にできるループ回して(append(pop(0)))で毎回比較とか
    assert same_path(sorted(reduction(castles["teamA"][0])), sorted(set(tops4_1)))


def test_judge_castle_3(judge, tops4_2):
    judge.build_castle("X", tops4_2)
    castles = judge.judge_castle()
    assert not(castles["teamA"])
    assert len(castles["teamB"]) == 1
    assert same_path(sorted(reduction(castles["teamB"][0])), sorted(set(tops4_2)))


def test_judge_zone_1(judge, tops4_1):
    judge.build_castle("O", tops4_1)
    zones = judge.judge_zone("O")
    assert zones["teamA"] == {(1, 1), }


def test_judge_zone_2(judge, tops6):
    judge.build_castle("O", tops6)
    zones = judge.judge_zone("O")
    assert zones["teamA"] == {(1, 1), (1, 2), (2, 1)}


def test_judge_zone_3(judge, tops8):
    judge.build_castle("O", tops8)
    zones = judge.judge_zone("O")
    assert zones["teamA"] == {(2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (3, 2), (3, 6), (4, 2), (4, 6), (5, 2)}


def test_update(judge, mock_status, tops4_1):
    judge.build_castle("O", tops4_1)
    judge.update()
    for i in range(3):
        for j in range(3):
            if i == j == 1:
                mock_status[i][j] = "+"
            else:
                mock_status[i][j] = "O"
    assert judge.field.status == mock_status
