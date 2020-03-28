import pytest

from source.structure.room import Room

def test_can_instantiate_room(rectangle, test_area):
    """
    Test that the room can be instantiated and imported
    """
    assert Room
    new_room = Room(rectangle, 0, 1, 1, test_area, 'bathroom')
    assert isinstance(new_room, Room)

def test_point_in_room(rectangle,big_area):
    """
    Test that contains point returns true when point is in room
    """
    new_room = Room(rectangle, 0, 1, 1, big_area, 'bathroom')
    point = (0, 2, 2)
    assert new_room.contains_point(point[0], point[1], point[2]) is True

def test_point_not_in_room(rectangle, big_area):
    """
    Test that contains point returns false when point is not in room
    """
    new_room = Room(rectangle, 0, 1, 1, big_area, 'bathroom')
    point = (0, 15, 15)
    assert new_room.contains_point(point[0], point[1], point[2]) is False

def test_rectangle_intersects(rectangle, big_area):
    """
    Test that intersecting rectangles return true
    """
    new_room = Room(rectangle, 0, 1, 1, big_area, 'bathroom')
    rectangle = (0, 2, 15, 2, 15)
    assert new_room.contains_rectangle(rectangle[0], rectangle[1], rectangle[2], rectangle[3], rectangle[4]) is True

def test_rectangle_not_ntersects(rectangle, big_area):
    """
    Test that non-intersecting rectangles return false
    """
    new_room = Room(rectangle, 0, 1, 1, big_area, 'bathroom')
    rectangle = (0, 20, 25, 20, 25)
    assert new_room.contains_rectangle(rectangle[0], rectangle[1], rectangle[2], rectangle[3], rectangle[4]) is False
