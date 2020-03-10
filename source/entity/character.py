from source.entity.drawableEntity import DrawableEntity
from source.entity.component.moveable import Moveable

class Character(DrawableEntity):
    def __init__(self, z:int, x:int, y:int, char:str, color:tuple, *components):
        moveable:Moveable = Moveable(1)
        DrawableEntity.__init__(self, z, x, y, char, color, moveable, *components)
    
    def attempt_move(self, dz:int, dx:int, dy:int, area):
        return self.get(Moveable).attempt_move(self, area, dz, dx, dy)
    
    def move(self, dz:int, dx:int, dy:int, area):
        return self.get(Moveable).move(self, area, dz, dx, dy)
