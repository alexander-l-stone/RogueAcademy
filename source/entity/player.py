from source.entity.character import Character
from source.entity.component.moveable import Moveable

class Player(Character):
    def __init__(self, z:int, x:int, y:int, char:str, color:tuple, *components):
        Character.__init__(self, z, x, y, char, color, *components)
        self.set(Moveable(1))