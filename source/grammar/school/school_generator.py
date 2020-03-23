import random
import numpy
from typing import List

from source.grammar.GrammarRule import GrammarRule, GrammarVariable
from source.area.area import Area
from source.grammar.school.blueprint import Rectangle
from source.structure.room import Room
import source.grammar.school.room_generator

#Grid Size currently must be at least 17 and divides evenly into both the height and width of the area
GRID_SIZE: int = 20

#TODO: Overhaul great hall generation

#Grammar Library for SchoolGenerator
rule_great_hall_size = GrammarRule("size_hall", [[max(10,GRID_SIZE-4)],[max(15,GRID_SIZE-2)]])
# z x y floorTile
rule_great_hall = GrammarRule("great_hall", [[1, rule_great_hall_size, rule_great_hall_size, 1, 0]], None, lambda sel: Rectangle.create(sel))
# great_hall_ref = GrammarVariable('great_hall')

rule_room_type = GrammarRule("room_type", [["bathroom"], ["classroom"], ["storage_room"]])

# options 3, 6, 1

rule_num_rooms = GrammarRule("num_rooms", [[]], None, lambda sel : [rule_room_type for i in range(0,random.randint(49,51))])
# print(f"NUM_ROOMS = {GrammarRule.generate(rule_num_rooms)}")
rule_school = GrammarRule("root", [[rule_great_hall, rule_num_rooms]])

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
    def carve_v_corridor(y1: int, y2: int, x: int, z: int, floor_int: int, area: Area):
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
        rooms:List[Rectangle] = GrammarRule.generate(rule_school)
        
        room_list:List[Room] = []

        grid_point:List[tuple] = []
        xy_coords:List[tuple] = []
        prev_elem:Rectangle = None
        for x in range(0,area.x_length+1, GRID_SIZE):
            for y in range(0,area.y_length+1, GRID_SIZE):
                if(x >= 0 and x < area.x_length and y >= 0 and y < area.y_length):
                    grid_point.append((x, y))
        for elem in rooms:
            #randZ = random.randrange(1 + elem.z_length, area.z_length - 2 - elem.z_length)
            grid_coords = random.choice(grid_point)
            grid_point.remove(grid_coords)
            elem.x_corner = random.randrange(grid_coords[0]+1, grid_coords[0]+GRID_SIZE-elem.x_length)
            elem.y_corner = random.randrange(grid_coords[1]+1, grid_coords[1]+GRID_SIZE-elem.y_length)
            xy_coords.append((random.randrange(elem.x_corner, elem.x_corner + elem.x_length), random.randrange(elem.y_corner, elem.y_corner + elem.y_length), elem.z_length, elem.floortype))
            #Replace the prexisting tile with the floor_tile of the elem
            for x in range(elem.x_corner, elem.x_corner + elem.x_length):
                for y in range(elem.y_corner, elem.y_corner + elem.y_length):
                    area.map[0, x, y] = elem.floortype
            room_list.append(Room(elem, 0, elem.x_corner,elem.y_corner, area, room_type=GrammarRule.generate(rule_room_type)[0]))

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
        room_list[0].room_type = "great_hall"
        for structure in room_list:
            #Refloor every room with its floor
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
        return rooms
