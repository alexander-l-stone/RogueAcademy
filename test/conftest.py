import pytest

from source.area.area import Area
from source.entity.drawableEntity import DrawableEntity
from source.entity.character import Character
from source.action.action import Action
from source.entity.player import Player
from source.grammar.school.blueprint import Rectangle

@pytest.fixture
def test_area():
    area = Area(1, 10, 10)
    area.map[0,2,2] = 1
    area.map[0,1,2] = 1
    area.map[0,1,1] = 1
    area.map[0,2,1] = 1
    return area

@pytest.fixture
def test_entity():
    return DrawableEntity(0, 1, 1, 't', (255, 255, 255))

@pytest.fixture
def action():
    return Action('me', 1)

@pytest.fixture
def long_action():
    return Action('long', 2)

@pytest.fixture
def player():
    return Player(0, 1, 1, '@', (255, 255, 255))

@pytest.fixture
def rectangle():
    return Rectangle(1, 5, 5, 1, 0)