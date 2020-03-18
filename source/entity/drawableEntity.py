from source.entity.entity import Entity
import tcod

class DrawableEntity(Entity):
    def __init__(self, z:int, x:int, y:int, char:str, color:tuple, *components):
        Entity.__init__(self, *components)
        self.x:int = x
        self.y:int = y
        self.z:int = z
        self.char:str = char
        self.color:tuple = color
    
    def draw(self, topx, topy) -> None:
        tcod.console_set_default_foreground(0, self.color)
        #find the offset coordinates and draw to that point on the screen
        tcod.console_put_char(0, self.x-topx, self.y-topy, self.char, tcod.BKGND_NONE)