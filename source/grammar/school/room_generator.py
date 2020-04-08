import random
from typing import List,Dict
import copy

from source.grammar.school.blueprint import Rectangle
from source.grammar.GrammarRule import GrammarRule, GrammarVariable
from source.structure.room import Room
from source.entity.entity import Entity

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

rule_bathroom_entity = GrammarRule("bathroom_entity", [
    [Entity(-1, -1, -1, chr(129), (240, 240, 240), {'blocks_movement':True})],
    [Entity(-1, -1, -1, '%', (200, 200, 240), {'blocks_movement': True})]])

rule_classroom_entity = GrammarRule("classroom_entity", [
    [Entity(-1, -1, -1, chr(254), (210, 180, 150), {'blocks_movement': True})]])

rule_storage_room_entity = GrammarRule("storage_room_entity", [
    [Entity(-1, -1, -1, chr(4), (193, 154, 107), {'blocks_vision': True})],
    [Entity(-1, -1, -1, chr(7), (193, 154, 107), {'blocks_vision': True})]])

class RoomGenerator:
    """
    Randomly generates a room
    """
    def __init__(self, room:Rectangle):
        self.room:Rectangle = room

    @staticmethod
    def generate_room(z:int, x:int, y:int, area, room_type:str) -> Room:
        """
        Generate a Room
        """
        num_entities:int = 0
        if room_type == 'bathroom':
            num_entities = random.randrange(1, 6)
            blueprint:Rectangle = GrammarRule.generate(rule_room_bathroom)[0]
        elif room_type == 'classroom':
            num_entities = random.randrange(4, 11)
            blueprint:Rectangle = GrammarRule.generate(rule_room_classroom)[0]
        elif room_type == 'storage_room':
            num_entities = random.randrange(30, 90)
            blueprint:Rectangle = GrammarRule.generate(rule_room_storage_room)[0]
        elif room_type == 'great_hall':
            blueprint:Rectangle = GrammarRule.generate(rule_great_hall)[0]
        elif(blueprint is None):
            raise TypeError
        x_corner:int = random.randrange(max(0,x+1), min(area.x_length-1, x+GRID_SIZE-blueprint.x_length))
        y_corner:int = random.randrange(max(0,y+1), min(area.y_length-1, y+GRID_SIZE-blueprint.y_length))
        for x in range(x_corner, x_corner + blueprint.x_length):
            for y in range(y_corner, y_corner + blueprint.y_length):
                area.map[0, x, y] = blueprint.floortype
        if room_type == 'bathroom':
            for i in range(0, num_entities+1):
                new_entity:Entity = copy.deepcopy(GrammarRule.generate(rule_bathroom_entity)[0])
                x = random.randrange(max(1,x_corner+1), min(area.x_length-1,x_corner+blueprint.x_length))
                y = random.randrange(max(1, y_corner+1), min(area.y_length-1, y_corner+blueprint.y_length))
                new_entity.z = z
                new_entity.x = x
                new_entity.y = y
                area.add_object(new_entity)
        elif room_type == 'classroom':
            for i in range(0, num_entities+1):
                new_entity: Entity = copy.deepcopy(GrammarRule.generate(rule_classroom_entity)[0])
                x = random.randrange(max(1, x_corner+1), min(area.x_length-1, x_corner+blueprint.x_length))
                y = random.randrange(max(1, y_corner+1), min(area.y_length-1, y_corner+blueprint.y_length))
                new_entity.z = z
                new_entity.x = x
                new_entity.y = y
                area.add_object(new_entity)
        elif room_type == 'storage_room':
            for i in range(0, num_entities+1):
                new_entity:Entity = copy.deepcopy(GrammarRule.generate(rule_storage_room_entity)[0])
                x = random.randrange(max(1, x_corner+1), min(area.x_length-1, x_corner+blueprint.x_length))
                y = random.randrange(max(1, y_corner+1), min(area.y_length-1, y_corner+blueprint.y_length))
                new_entity.z = z
                new_entity.x = x
                new_entity.y = y
                area.add_object(new_entity)
        return Room(blueprint, 0, x_corner, y_corner, area, room_type=room_type)
