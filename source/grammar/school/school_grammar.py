import random
import numpy
from typing import List

from source.grammar.GrammarRule import GrammarRule, GrammarVariable
from source.area.area import Area
from source.grammar.school.room import Room

#TODO: Overhaul great hall generation

#Grammar Library for SchoolGenerator
rule_great_hall_size = GrammarRule([[15],[18]], "size_hall")
# z x y floorTile
rule_great_hall = GrammarRule([[1, rule_great_hall_size, rule_great_hall_size, 1, 0]], "great_hall", None, lambda sel: Room.create(sel))
# great_hall_ref = GrammarVariable('great_hall')

rule_room_size = GrammarRule([[]], "size", None, lambda sel : random.randint(3,14))
rule_room_floor = GrammarRule([[1], [3]], "floor")
rule_room_wall = GrammarRule([[0]], "wall")
# z x y floorTile
rule_room = GrammarRule([[1, rule_room_size, rule_room_size, rule_room_floor, rule_room_wall]], "room", None, lambda sel: Room.create(sel))

# options 3, 6, 1
rule_num_rooms = GrammarRule([[]], "num_rooms", None, lambda sel : [rule_room for i in range(0,random.randint(23,24))])
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
        for x in range(min(x1, x2), max(x1, x2)+1):
            area.map[z, x, y] = floor_int
    
    @staticmethod
    def carve_v_corridor(y1: int, y2: int, x: int, z: int, floor_int: int, area: Area):
        """
        Carve a vertical corridor from z, x, y1 to z, x, y2
        """
        for y in range(min(y1, y2), max(y1, y2)+1):
            area.map[z, x, y] = floor_int
    
    @staticmethod
    def connect_points(z:int, x1:int, x2:int, y1:int, y2:int, floor_int:int, area:Area):
        """
        Connects two points using horizontal and vertical corridors
        """
        if(random.randrange(0, 2) != 1):
            #Do horizontal first
            SchoolGenerator.carve_h_corridor(x1, x2, y1, z, floor_int, area)
            SchoolGenerator.carve_v_corridor(y1, y2, x2, z, floor_int, area)
        else:
            #Do vertical first
            SchoolGenerator.carve_v_corridor(y1, y2, x1, z, floor_int, area)
            SchoolGenerator.carve_h_corridor(x1, x2, y2, z, floor_int, area)

    # Make a Great Hall, and some number of rooms. Ensure that you can get from any room to any other room and that the great hall is connected to this network
    @staticmethod
    def generate_school(area:Area):
        rooms:List[Room] = GrammarRule.generate(rule_school)
        
        grid_size:int = 20
        grid_point:List[tuple] = []
        xy_coords:List[tuple] = []
        prev_elem:Room = None
        for x in range(0,area.x_length+1, grid_size):
            for y in range(0,area.y_length+1, grid_size):
                if(x >= 0 and x < area.x_length and y >= 0 and y < area.y_length):
                    grid_point.append((x, y))
        print(f"Grid Points: {len(grid_point)}")
        for elem in rooms:
            #randZ = random.randrange(1 + elem.z_length, area.z_length - 2 - elem.z_length)
            grid_coords = random.choice(grid_point)
            grid_point.remove(grid_coords)
            elem.x_corner = random.randrange(grid_coords[0]+1, grid_coords[0]+grid_size-elem.x_length)
            elem.y_corner = random.randrange(grid_coords[1]+1, grid_coords[1]+grid_size-elem.y_length)
            #Replace the prexisting tile with the floor_tile of the elem
            xy_coords.append((random.randrange(elem.x_corner, elem.x_corner + elem.x_length), random.randrange(elem.y_corner, elem.y_corner + elem.y_length), elem.z_length, elem.floortype))
            for x in range(elem.x_corner, elem.x_corner + elem.x_length):
                for y in range(elem.y_corner, elem.y_corner + elem.y_length):
                    area.map[0, x, y] = elem.floortype
            if(prev_elem != None):
                SchoolGenerator.connect_points(
                    0, 
                    random.randrange(elem.x_corner, elem.x_corner + elem.x_length), 
                    random.randrange(prev_elem.x_corner,prev_elem.x_corner + prev_elem.x_length),
                    random.randrange(elem.y_corner, elem.y_corner + elem.y_length),
                    random.randrange(prev_elem.y_corner,prev_elem.y_corner + prev_elem.y_length),
                    elem.floortype,
                    area,
                    )
            prev_elem = elem
        return rooms
