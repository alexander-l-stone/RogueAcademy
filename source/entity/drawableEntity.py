from source.entity.entity import Entity

class DrawableEntity(Entity):
    def __init__(self, x:int, y:int, char:str, color, *components):
        Entity.__init__(components)
        self.x:int = x
        self.y:int = y
        self.char:str = char
        self.color = color
    
    def draw(self, console):
        console.draw_char(self.x, self.y, self.char, self.color)