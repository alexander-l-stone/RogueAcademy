import numpy
import tcod

from source.entity.drawableEntity import DrawableEntity

class Area:
    def __init__(self, z_length: int, x_length: int, y_length: int, wall: DrawableEntity = DrawableEntity(-1, -1, -1, '#', (80, 80, 80), 'blocks_movement'), floor: DrawableEntity = DrawableEntity(-1, -1, -1, '.', (80, 80, 80))):
        self.x_length:int = x_length
        self.y_length:int = y_length
        if z_length < 1:
            self.z_length = 1
        else:
            self.z_length:int = z_length
        self.wall:DrawableEntity = wall
        self.floor:DrawableEntity = floor
        self.objdict:dict = {}
        # z x y
        self.map = numpy.array([[[True for y in range(self.y_length)] for x in range(self.x_length)] for z in range(self.z_length)])
    
    def draw(self, playerz, playerx, playery, screen_width, screen_height):
        corner_x = playerx-screen_width//2
        corner_y = playery-screen_height//2
        # Find the coordinates from the center point(the player) to the top and bottom of the screen
        for drawx in range(playerx-screen_width//2, playerx+screen_width//2):
            for drawy in range(playery-screen_height//2, playery+screen_height//2):
                #If an object is there, draw it.
                #TODO: Make walls hide objects maybe???
                if self.objdict.get((playerz,drawx,drawy)):
                    print(f"drawing entity: {self.objdict[(playerz,drawx,drawy)].char}")
                    self.objdict[(playerz,drawx,drawy)].draw(corner_x, corner_y)
                else:
                    #Try Catch for drawing stuff outside the area
                    #TODO: Better handling for stuff not in this structure
                    try:
                        #If the map point exists its a wall
                        if self.map[playerz][drawx][drawy]:
                            #Set the default wall's coordinates to the correct ones
                            self.wall.z = playerz
                            self.wall.x = drawx
                            self.wall.y = drawy
                            #Draw it
                            self.wall.draw(corner_x, corner_y)
                        else:
                            #Set the default floor's coordinates to the correct ones
                            self.floor.z = playerz
                            self.floor.x = drawx
                            self.floor.y = drawy
                            #Draw it
                            self.floor.draw(corner_x, corner_y)
                    except IndexError:
                        #Draw blank space if nothing is expected there
                        tcod.console_set_default_foreground(0, tcod.black)
                        tcod.console_put_char(0, drawx, drawy, ' ', tcod.BKGND_NONE)
