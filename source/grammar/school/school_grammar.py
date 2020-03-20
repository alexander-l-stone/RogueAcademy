import random
import numpy
from typing import List

from source.grammar.GrammarRule import GrammarRule, GrammarVariable
from source.area.area import Area
from source.grammar.school.room import Room

#Grammar Library for SchoolGenerator
rule_great_hall_size = GrammarRule([[30],[40]], "size_hall")
# z x y floorTile
rule_great_hall = GrammarRule([[1, rule_great_hall_size, rule_great_hall_size, 1]], "great_hall", None, lambda sel: Room.create(sel))
# great_hall_ref = GrammarVariable('great_hall')

rule_room_size = GrammarRule([[]], "size", None, lambda sel : random.randint(3,14))
# z x y floorTile
rule_room = GrammarRule([[1, rule_room_size, rule_room_size, 1]], "room", None, lambda sel: Room.create(sel))

# options 3, 6, 1
rule_num_rooms = GrammarRule([[]], "num_rooms", None, lambda sel : [rule_room for i in range(0,random.randint(3,20))])
# print(f"NUM_ROOMS = {GrammarRule.generate(rule_num_rooms)}")
rule_school = GrammarRule([[rule_great_hall, rule_num_rooms]], "root")

#TODO: Make this just a generate_school function
class SchoolGenerator:
    """
    Randomly generates a school
    """
    def __init__(self, area:Area):
        self.area = area

    @staticmethod
    def carve_h_corridor(x1:int, x2:int, y:int, z:int, floor_int:int, area:Area):
        """
        Carve a horizontal corridor from z, x1, y to z, x2, y
        """
        # print(f"Floor int: {floor_int}")
        for x in range(min(x1, x2), max(x1, x2)):
            area.map[z, x, y] = floor_int
    
    @staticmethod
    def carve_v_corridor(y1: int, y2: int, x: int, z: int, floor_int: int, area: Area):
        """
        Carve a vertical corridor from z, x, y1 to z, x, y2
        """
        for y in range(min(y1, y2), max(y1, y2)):
            area.map[z, x, y] = floor_int

    # Make a Great Hall, and some number of rooms. Ensure that you can get from any room to any other room and that the great hall is connected to this network
    @staticmethod
    def generate_school(area:Area):
        rooms:List[Room] = GrammarRule.generate(rule_school)
        
        xy_coords = []
        for elem in rooms:
            #randZ = random.randrange(1 + elem.z_length, area.z_length - 2 - elem.z_length)
            elem.x_corner = random.randrange(1 + elem.x_length, area.x_length - 2 - elem.x_length)
            elem.y_corner = random.randrange(1 + elem.y_length, area.y_length - 2 - elem.y_length)
            #Replace the prexisting tile with the floor_tile of the elem
            xy_coords.append((random.randrange(elem.x_corner, elem.x_corner + elem.x_length), random.randrange(elem.y_corner, elem.y_corner + elem.y_length), elem.z_length, elem.tiletype))
            for x in range(elem.x_corner, elem.x_corner + elem.x_length):
                for y in range(elem.y_corner, elem.y_corner + elem.y_length):
                    area.map[0, x, y] = elem.tiletype
            #Connect all rooms
        while(len(xy_coords) >= 2):
            curr_coords = xy_coords.pop()
            if (random.randrange(0, 3) == 0):
                #Do X first
                SchoolGenerator.carve_h_corridor(curr_coords[0], xy_coords[0][0], curr_coords[1], 0, curr_coords[3], area)
                SchoolGenerator.carve_v_corridor(curr_coords[1], xy_coords[0][1], xy_coords[0][0], 0, curr_coords[3], area)
            else:
                #Do Y First
                SchoolGenerator.carve_v_corridor(curr_coords[1], xy_coords[0][1], curr_coords[0], 0, curr_coords[3], area)
                SchoolGenerator.carve_h_corridor(curr_coords[0], xy_coords[0][0], xy_coords[0][1], 0, curr_coords[3], area)
        return rooms
