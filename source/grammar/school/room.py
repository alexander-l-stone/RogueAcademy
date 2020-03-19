from typing import List

class Room:
    def __init__(self, z_length:int, x_length:int, y_length:int, tiletype:int):
        self.z_length = z_length
        self.x_length = x_length
        self.y_length = y_length
        self.tiletype = tiletype

    @staticmethod
    def create(selection:List[int]):
        return Room(selection[0], selection[1], selection[2], selection[3])