import numpy
import tcod

from source.entity.drawableEntity import DrawableEntity

class Area:
    def __init__(self, x_length: int, y_length: int, z_length: int=1, wall: DrawableEntity = DrawableEntity(-1, -1, -1, '#', (80, 80, 80), 'blocks_movement'), floor: DrawableEntity = DrawableEntity(-1, -1, -1, '.', (80, 80, 80))):
        self.x_length:int = x_length
        self.y_length:int = y_length
        self.z_length:int = z_length
        self.wall:DrawableEntity = wall
        self.floor:DrawableEntity = floor
        self.objdict:dict = {}
        self.map = numpy.array([[[True for x in range(self.x_length)] for y in range(self.y_length)] for z in range(self.z_length)])
    
    def draw(self, playerx, playery, playerz, screen_width, screen_height):
        # Find the coordinates from the center point(the player) to the top and bottom of the screen
        for drawx in range(playerx-screen_width//2, playerx+screen_width//2):
            for drawy in range(playery-screen_height//2, playery+screen_height//2):
                print(f"{drawx},{drawy},{playerz}")
                #If an object is there, draw it.
                #TODO: Make walls hide objects maybe???
                if (self.objdict.get((drawx, drawy, playerz))):
                    self.objdict[(drawx, drawy, playerz)].draw(playerx-screen_width//2, playery-screen_height//2)
                else:
                    #Try Catch for drawing stuff outside the area
                    #TODO: Better handling for stuff not in this structure
                    try:
                        #If the map point exists its a wall
                        if(self.map[drawx][drawy][playerz]):
                            #Set the default wall's coordinates to the correct ones
                            self.wall.x = drawx
                            self.wall.y = drawy
                            self.wall.z = playerz
                            #Draw it
                            self.wall.draw(playerx-screen_width//2, playery-screen_height//2)
                        else:
                            #Set the default floor's coordinates to the correct ones
                            self.floor.x = drawx
                            self.floor.y = drawy
                            self.floor.z = playerz
                            #Draw it
                            self.floor.draw(playerx-screen_width//2, playery-screen_height//2)
                    except IndexError:
                        #Draw blank space if nothing is expected there
                        tcod.console_set_default_foreground(0, tcod.black)
                        tcod.console_put_char(0, drawx, drawy, ' ', tcod.BKGND_NONE)
