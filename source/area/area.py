import numpy
import tcod

from source.entity.drawableEntity import DrawableEntity

class Area:
    def __init__(self, x_length: int, y_length: int, z_length: int=1, wall: DrawableEntity = DrawableEntity(-1, -1, -1, '#', (80, 80, 80), 'blocks_movement'), floor: DrawableEntity = DrawableEntity(-1, -1, -1, '.', (80, 80, 80))):
        self.x_length:int = x_length
        self.y_length:int = y_length
        self.z_length:int = z_length
        self.wall = wall
        self.floor = floor
        self.objdict = {}
        self.map = numpy.array([[[False for x in range(self.x_length)] for y in range(self.y_length)] for z in range(self.z_length)])
    
    def draw(self, playerx, playery, playerz, screen_width, screen_height):
        print(self.map)
        for drawx in range(playerx-screen_width//2, playerx+screen_width//2):
            for drawy in range(playery-screen_height//2, playery+screen_height//2):
                if (self.objdict.get((drawx, drawy, playerz))):
                    self.objdict[(drawx, drawy, playerz)].draw(playerx-screen_width//2, playery-screen_height//2)
                else:
                    try:
                        if(self.map[drawx][drawy][playerz]):
                            self.wall.x = drawx
                            self.wall.y = drawy
                            self.wall.z = playerz
                            self.wall.draw(playerx-screen_width//2, playery-screen_height//2)
                        else:
                            self.floor.x = drawx
                            self.floor.y = drawy
                            self.floor.z = playerz
                            self.floor.draw(playerx-screen_width//2, playery-screen_height//2)
                    except IndexError:
                        tcod.console_set_default_foreground(0, tcod.black)
                        tcod.console_put_char(0, drawx, drawy, ' ', tcod.BKGND_NONE)


        self.wall.x = -1
        self.wall.y = -1
        self.wall.z = -1
        self.floor.x = -1
        self.floor.y = -1
        self.floor.z = -1
