from source.entity.entity import Entity
import tcod

class DrawableEntity(Entity):
    def __init__(self, x:int, y:int, char:str, color:tuple, *components):
        Entity.__init__(self, *components)
        self.x:int = x
        self.y:int = y
        self.char:str = char
        self.color:tuple = color
    
    def draw(self):
        tcod.console_set_default_foreground(0, tcod.white)
        tcod.console_put_char(0, self.x, self.y, self.char, tcod.BKGND_NONE)
