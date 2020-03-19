import pytest
from source.entity.entity import Entity

def test_can_instantiate_entity():
    assert Entity
    test_entity = Entity()
    assert isinstance(test_entity, Entity)

def test_cannot_grab_nonexisting_component_from_entity():
    test_entity = Entity()
    assert test_entity.has(IntComponent) is False

def test_cannot_grab_nonexisting_string_component_from_entity():
    test_entity = Entity()
    assert test_entity.has("blocks_vision") is False

def test_can_grab_existing_component():
    test_component = IntComponent(2)
    test_entity = Entity(test_component)
    assert test_entity.has(IntComponent) is True
    assert test_entity.get(IntComponent).value is 2

def test_can_grab_string_component():
    test_entity = Entity("blocks_movement")
    assert test_entity.has("blocks_movement") is True
    assert test_entity.get("blocks_movement") is True

def test_cannot_grab_wrong_string_component():
    test_entity = Entity("blocks_movement")
    assert test_entity.has("blocks_movement") is True
    assert test_entity.has("blocks_vision") is False

class IntComponent:
    def __init__(self, value):
        self.value = value
