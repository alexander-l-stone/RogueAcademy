from typing import List

class Blueprint:
    def __init__(self):
        pass

    @staticmethod
    def create(selection:List[int]):
        pass

class Rectangle(Blueprint):
    def __init__(self, z_length:int, x_length:int, y_length:int, floortype:int, walltype:int):
        Blueprint.__init__(self)
        self.z_length:int = z_length
        self.x_length:int = x_length
        self.y_length:int = y_length
        self.floortype:int = floortype
        self.walltype:int = walltype

    @staticmethod
    def create(selection:List[int]):
        return Rectangle(selection[0], selection[1], selection[2], selection[3], selection[4])