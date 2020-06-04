from judge.agent import Agent
from judge.field import Point
import pytest


@pytest.fixture
def agent(field):
    return Agent(field.size)


def test_agent_init(agent):
    assert agent.point is None
    assert not agent.on_field
    assert agent.next_activity is None


def test_agent_set_point_1(agent, field):
    agent.point = Point(0, 0)
    agent.point = Point(0, field.width - 1)
    agent.point = Point(field.height - 1, 0)
    assert True


def test_agent_set_point_2(agent, field):
    with pytest.raises(ValueError):
        agent.point = Point(field.height, 0)


def test_agent_set_point_3(agent, field):
    with pytest.raises(ValueError):
        agent.point = Point(0, field.width)


def test_agent_set_point_4(agent, field):
    with pytest.raises(ValueError):
        agent.point = Point(-1, -1)


def test_agent_set_point_5(agent, field):
    with pytest.raises(AttributeError):
        agent.point = (0, 0)


def test_agent_set_point_6(agent, field):
    with pytest.raises(AttributeError):
        agent.point = [0, 0]
