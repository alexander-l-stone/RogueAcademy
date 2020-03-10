import pytest

from source.area.area import Area
from source.entity.drawableEntity import DrawableEntity
from source.entity.character import Character

@pytest.fixture
def test_area():
    area = Area(1, 10, 10)
    area.map[0,2,2] = False
    area.map[0,1,2] = False
    area.map[0,1,1] = False
    area.map[0,2,1] = False
    return area

@pytest.fixture
def test_entity():
    return DrawableEntity(0, 1, 1, 't', (255, 255, 255))