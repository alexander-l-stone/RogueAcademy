import tcod

class Entity:
    """
    Basic game entity class that stores a drawable character on the map.

    Flags:

    blocks_movement: Boolean for if this is a wall or not.
    blocks_vision: Boolean for if this blocks vision or not

    water_mana_prod: Int for how much water mana is produced by this Entity.
    fire_mana_prod: Int for how much fire mana is produced by this Entity.
    earth_mana_prod: Int for how much earth mana is produced by this Entity.
    air_mana_prod: Int for how much air mana is produced by this Entity.
    dream_mana_prod: Int for how much dream mana is produced by this Entity.
    """
    def __init__(self, z:int, x:int, y:int, char:str, color:tuple, flags:dict=None, **kwargs):
        self.x:int = x
        self.y:int = y
        self.z:int = z
        self.char:str = char
        self.color:tuple = color
        if flags == None:
            self.flags = {}
        else:
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
