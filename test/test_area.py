from source.area.area import Area

def test_can_instantiate_area():
    assert Area
    area = Area(1,1,1)
    assert type(area) is Area

def test_can_add_and_get_object(test_entity):
    area = Area(2, 5, 5)
    area.add_object(test_entity)
    assert area.get_object(test_entity.z, test_entity.x, test_entity.y) is test_entity
