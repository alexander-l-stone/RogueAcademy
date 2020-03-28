import random
import numpy
from typing import List

from source.grammar.GrammarRule import GrammarRule, GrammarVariable
from source.area.area import Area
from source.grammar.school.blueprint import Rectangle
from source.structure.room import Room
from source.grammar.school.room_generator import RoomGenerator

#Grid Size currently must be at least 17 and divides evenly into both the height and width of the area
GRID_SIZE: int = 20

rule_room_type = GrammarRule("room_type", [["bathroom"], ["classroom"], ["storage_room"]])

# options 3, 6, 1

rule_num_rooms = GrammarRule("num_rooms", [[]], None, lambda sel : [rule_room_type for i in range(0,random.randint(49,51))])
# print(f"NUM_ROOMS = {GrammarRule.generate(rule_num_rooms)}")
rule_school = GrammarRule("root", [["great_hall", rule_num_rooms]])

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
            area.fov_map[z, x, y] = 1

    @staticmethod
    def carve_v_corridor(y1:int, y2:int, x:int, z:int, floor_int: int, area: Area):
        """
        Carve a vertical corridor from z, x, y1 to z, x, y2
        """
        for y in range(min(y1, y2), max(y1, y2)+1):
            area.map[z, x, y] = floor_int
            area.fov_map[z, x, y] = 1
    
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
        rooms:List[str] = GrammarRule.generate(rule_school)
        
        room_list:List[Room] = []

        grid_point:List[tuple] = []
        prev_elem:Room = None
        for x in range(0,area.x_length+1, GRID_SIZE):
            for y in range(0,area.y_length+1, GRID_SIZE):
                if(x >= 0 and x < area.x_length and y >= 0 and y < area.y_length):
                    grid_point.append((x, y))
        for elem in rooms:
            #randZ = random.randrange(1 + elem.z_length, area.z_length - 2 - elem.z_length)
            grid_coords = random.choice(grid_point)
            grid_point.remove(grid_coords)
            room_list.append(RoomGenerator.generate_room(0, grid_coords[0], grid_coords[1], area, elem))
            if(prev_elem != None):
                SchoolGenerator.connect_points(
                    0, 
                    random.randrange(room_list[-1].x1, room_list[-1].x2),
                    random.randrange(prev_elem.x1, prev_elem.x2),
                    random.randrange(room_list[-1].y1, room_list[-1].y2),
                    random.randrange(prev_elem.y1, prev_elem.y2),
                    1,
                    area,
                    )
            prev_elem = room_list[-1]
        for structure in room_list:
            #Refloor every room with its floor and add the walls
            #TODO: Fix the corners not getting walls
            for x in range(structure.x1, structure.x2):
                if(structure.y1 - 1 > 0 and area.tileset[area.map[structure.z, x, structure.y1 - 1]].has("blocks_movement")):
                    area.map[structure.z, x, structure.y1 - 1] = structure.wall
                if(area.tileset[area.map[structure.z, x, structure.y2]].has("blocks_movement")):
                    area.map[structure.z, x, structure.y2] = structure.wall
                for y in range(structure.y1, structure.y2):
                    area.map[structure.z, x, y] = structure.floor
                    if(structure.x1 - 1 > 0 and area.tileset[area.map[structure.z, structure.x1 - 1, y]].has("blocks_movement")):
                        area.map[structure.z, structure.x1-1, y] = structure.wall
                    if(area.tileset[area.map[structure.z, structure.x2, y]].has("blocks_movement")):
                        area.map[structure.z, structure.x2, y] = structure.wall
        #Create the FoV map at the end. 
        #TODO: Handle z
        for x in range(0, area.x_length):
            for y in range(0, area.y_length):
                point = area.map[0,x,y]
                if(not area.tileset[point].has("blocks_vision")):
                    area.fov_map[0, x, y] = 1
                else:
                    area.fov_map[0, x, y] = 0
                tile_objects = area.get_object(0, x, y)
                if(tile_objects):
                    for tile_obj in tile_objects:
                        if tile_obj.has("blocks_vision"):
                            area.fov_map[0, x, y] = 0
                            break
        return room_list
