from source.area.area import Area
from copy import deepcopy

def test_can_instantiate_area():
    assert Area
    area = Area(1,1,1)
    assert isinstance(area, Area)

def test_can_add_and_get_object(test_entity):
    area = Area(2, 5, 5)
    area.add_object(test_entity)
    assert area.get_object(test_entity.z, test_entity.x, test_entity.y) == [test_entity]

def test_can_add_and_get_multiple_objects(test_entity):
    copy_entity = deepcopy(test_entity)
    area = Area(2, 5, 5)
    area.add_object(test_entity)
    area.add_object(copy_entity)
    assert area.get_object(test_entity.z, test_entity.x,test_entity.y) == [test_entity, copy_entity]

def test_can_remove_entity(test_entity):
    area = Area(2, 5, 5)
    area.add_object(test_entity)
    assert area.get_object(test_entity.z, test_entity.x, test_entity.y) == [test_entity]
    area.remove_object(test_entity)
    assert area.get_object(test_entity.z, test_entity.x, test_entity.y) == None
