# from typing import List
from source.entity.drawableEntity import DrawableEntity
from source.grammar.school.blueprint import Blueprint
from source.area.area import Area

#TODO: Make Room handle non square shapes
class Room:
    def __init__(self, blueprint:Blueprint, z:int, x:int, y:int, area:Area, room_type:str="Empty"):
        self.x1:int = x
        self.x2:int = self.x1 + blueprint.x_length
        self.y1:int = y
        self.y2:int = self.y1 + blueprint.y_length
        self.z:int = z
        self.area:Area = area
        self.room_type:str = room_type
        self.floor = blueprint.floortype
        self.wall = blueprint.walltype
    
    def generate_room(self) -> None:
        if self.room_type == 'bathroom':
            center_x:int = (self.x1+self.x2)//2
            center_y:int = (self.y1+self.y2)//2
            new_entity = DrawableEntity(self.z, center_x, center_y, 'b', (0, 255, 0))
            self.area.add_object(new_entity)
        elif self.room_type == 'classroom':
            center_x:int = (self.x1+self.x2)//2
            center_y:int = (self.y1+self.y2)//2
            new_entity = DrawableEntity(self.z, center_x, center_y, 'c', (0, 255, 0))
            self.area.add_object(new_entity)
        elif self.room_type == 'storage_room':
            center_x:int = (self.x1+self.x2)//2
            center_y:int = (self.y1+self.y2)//2
            new_entity = DrawableEntity(self.z, center_x, center_y, 's', (0, 255, 0))
            self.area.add_object(new_entity)
        elif self.room_type == 'great_hall':
            center_x:int = (self.x1+self.x2)//2
            center_y:int = (self.y1+self.y2)//2
            new_entity = DrawableEntity( self.z, center_x, center_y, 'G', (0, 255, 0))
            self.area.add_object(new_entity)

    def contains_point(self, z, x, y) -> bool:
        """
        Check if a given point is inside this room
        """
        if(z != self.z):
            return False
        if(self.x1 < x and self.x2 > x) and (self.y1 < y and self.y2 > y):
            return True
        else:
            return False

    def contains_rectangle(self, z, x1, x2, y1, y2):
        """
        Checks if a given rectangle overlaps me
        """
        if(z != self.z):
            return False
        if(self.x1 <= x2 and self.x2 >= x1 and self.y1 <= y2 and self.y2 >= y1):
            return True
        else:
            return False