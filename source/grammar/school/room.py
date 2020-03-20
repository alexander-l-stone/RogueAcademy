from typing import List

class Room:
    def __init__(self, z_length:int, x_length:int, y_length:int, floortype:int, walltype:int):
        self.z_length = z_length
        self.x_length = x_length
        self.y_length = y_length
        self.floortype = floortype
        self.walltype = walltype

    @staticmethod
    def create(selection:List[int]):
        return Room(selection[0], selection[1], selection[2], selection[3], selection[4])