from source.entity.entity import Entity

class DrawableEntity(Entity):
    def __init__(self, x, y, char, color, *components):
        Entity.__init__(components)
        self.x = x
        self.y = y
        self.char = char
        self.color = color
    
    def draw(self, console):
        console.draw_char(self.x, self.y, self.char, self.color)