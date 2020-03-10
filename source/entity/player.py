from source.entity.character import Character

class Player(Character):
    def __init__(self, z:int, x:int, y:int, char:str, color:tuple, *components):
        Character.__init__(self, z, x, y, char, color, *components)