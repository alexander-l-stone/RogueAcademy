import random
from typing import List,Dict

from source.grammar.school.blueprint import Rectangle
from source.grammar.GrammarRule import GrammarRule, GrammarVariable
from source.structure.room import Room

GRID_SIZE: int = 20

rule_great_hall_size = GrammarRule("size_hall", [[max(10, GRID_SIZE-4)], [max(15, GRID_SIZE-2)]])
# z x y floorTile
rule_great_hall = GrammarRule("great_hall", [[1, rule_great_hall_size, rule_great_hall_size, 1, 0]], None, lambda sel: Rectangle.create(sel))

rule_bathroom_size = GrammarRule("size", [[3], [8]])
rule_bathroom_floor = GrammarRule("floor", [[5]])
rule_bathroom_wall = GrammarRule("wall", [[4]])
# z x y floorTile
rule_room_bathroom = GrammarRule("bathroom", [[1, rule_bathroom_size, rule_bathroom_size, rule_bathroom_floor, rule_bathroom_wall]], None, lambda sel: Rectangle.create(sel))

rule_classroom_size = GrammarRule("size", [[10], [16]])
rule_classroom_floor = GrammarRule("floor", [[3]])
rule_classroom_wall = GrammarRule("wall", [[2]])

rule_room_classroom = GrammarRule('classroom', [[1, rule_classroom_size, rule_classroom_size,rule_classroom_floor, rule_classroom_wall]], None, lambda sel: Rectangle.create(sel))

rule_storage_room_size = GrammarRule("size", [[5], [16]])
rule_storage_room_floor = GrammarRule("floor", [[1]])
rule_storage_room_wall = GrammarRule("wall", [[0]])

rule_room_storage_room = GrammarRule('storage_room', [[1, rule_storage_room_size, rule_storage_room_size, rule_storage_room_floor, rule_storage_room_wall]], None, lambda sel: Rectangle.create(sel))

rule_room_type = GrammarRule("room_type", [["bathroom"], ["classroom"], ["storage_room"]])


class RoomGenerator:
    """
    Randomly generates a room
    """
    def __init__(self, room:Rectangle):
        self.room = room

    @staticmethod
    def generate_room(z, x, y, area, room_type) -> Room:
        """
        Generate a Room
        """
        if room_type == 'bathroom':
            blueprint:Rectangle = GrammarRule.generate(rule_room_bathroom)[0]
        elif room_type == 'classroom':
            blueprint:Rectangle = GrammarRule.generate(rule_room_classroom)[0]
        elif room_type == 'storage_room':
            blueprint:Rectangle = GrammarRule.generate(rule_room_storage_room)[0]
        elif room_type == 'great_hall':
            blueprint:Rectangle = GrammarRule.generate(rule_great_hall)[0]
        elif(blueprint is None):
            raise TypeError
        x_corner: int = random.randrange(x+1, x+GRID_SIZE-blueprint.x_length)
        y_corner: int = random.randrange( y+1, y+GRID_SIZE-blueprint.y_length)
        for x in range(x_corner, x_corner + blueprint.x_length):
            for y in range(y_corner, y_corner + blueprint.y_length):
                area.map[0, x, y] = blueprint.floortype
        return Room(blueprint, 0, x_corner, y_corner, area, room_type=room_type)
