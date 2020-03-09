from source.entity.entity import Entity
import tcod

class DrawableEntity(Entity):
    def __init__(self, x:int, y:int, z:int, char:str, color:tuple, *components):
        Entity.__init__(self, *components)
        self.x:int = x
        self.y:int = y
        self.z:int = z
        self.char:str = char
        self.color:tuple = color
    
    def draw(self, topx, topy):
        tcod.console_set_default_foreground(0, self.color)
        tcod.console_put_char(0, self.x-topx, self.y-topy, self.char, tcod.BKGND_NONE)
