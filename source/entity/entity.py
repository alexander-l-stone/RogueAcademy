import tcod

class Entity:
    def __init__(self, z:int, x:int, y:int, char:str, color:tuple, flags:dict, **kwargs):
        self.x:int = x
        self.y:int = y
        self.z:int = z
        self.char:str = char
        self.color:tuple = color
        self.flags = flags
        if('explored_color' not in kwargs):
            self.explored_color = (max(30, color[0]-80), max(30, color[1]-80), max(30, color[2]-80))
        else:
            self.explored_color = kwargs['explored_color']
    
    def draw(self, topx, topy, override_color=None) -> None:
        if(override_color is None):
            tcod.console_set_default_foreground(0, self.color)
        else:
            tcod.console_set_default_foreground(0, override_color)
        #find the offset coordinates and draw to that point on the screen
        tcod.console_put_char(0, self.x-topx, self.y-topy, self.char, tcod.BKGND_NONE)

    def explored_draw(self, topx, topy) -> None:
        tcod.console_set_default_foreground(0, self.explored_color)
        #find the offset coordinates and draw to that point on the screen
        tcod.console_put_char(0, self.x-topx, self.y-topy,self.char, tcod.BKGND_NONE)
