import numpy
import tcod

from typing import List
from source.entity.drawableEntity import DrawableEntity

class Area:
    def __init__(self, z_length: int, x_length: int, y_length: int, tileset:dict = {1: DrawableEntity(-1, -1, -1, '.', (100,100,100)), 0: DrawableEntity(-1, -1, -1, '#', (100,100,100), 'blocks_movement', 'blocks_vision')}):
        self.x_length:int = x_length
        self.y_length:int = y_length
        if z_length < 1:
            self.z_length = 1
        else:
            self.z_length:int = z_length
        self.tileset:dict = tileset
        self.objdict:dict = {}
        # z x y
        self.map = numpy.array([[[0 for y in range(self.y_length)] for x in range(self.x_length)] for z in range(self.z_length)])
    
    def make_fov_map(self, playerz, playerx, playery, screen_width, screen_height) -> numpy.array:
        """
        Makes a fov transparency map out of the screen shown to the user
        """
        fov_array = numpy.array([[1 for y in range(screen_height)] for x in range(screen_width)])
        corner_x = playerx-screen_width//2
        corner_y = playery-screen_height//2
        for drawx in range(corner_x, playerx+screen_width//2):
            for drawy in range(corner_y, playery+screen_height//2):
                if(drawx >= 0 and drawx < self.x_length and drawy >= 0 and drawy < self.y_length):
                    tile = self.tileset[self.map[playerz, drawx, drawy]]
                    if (tile.get('blocks_vision') == True):
                        fov_array[drawx - corner_x][drawy - corner_y] = 0
        return tcod.map.compute_fov(fov_array, (screen_width//2, screen_height//2), 5)

    def add_object(self, entity:DrawableEntity) -> None:
        """
            Adds an entity to a square.
        """
        if (self.objdict.get((entity.z, entity.x, entity.y))):
            self.objdict[(entity.z, entity.x, entity.y)].append(entity)
        else:
            self.objdict[(entity.z, entity.x, entity.y)] = [entity]
    
    def get_object(self, z:int, x:int, y:int) -> List[DrawableEntity]:
        """
            Gets the list of entities at the given coordinates
        """
        return self.objdict.get((z, x, y))
    
    def remove_object(self,entity:DrawableEntity) -> bool:
        """
            Removes an entity from objdict

            Returns true if it was removed, false otherwise
        """
        entity_list = self.objdict.get((entity.z, entity.x, entity.y))
        if (entity in entity_list):
            entity_list.remove(entity)
            if len(entity_list) == 0:
                del self.objdict[(entity.z, entity.x, entity.y)]
            return True
        else:
            return False
        

    def draw(self, playerz, playerx, playery, screen_width, screen_height) -> None:
        corner_x = playerx-screen_width//2
        corner_y = playery-screen_height//2
        fov_map = self.make_fov_map(playerz, playerx, playery, screen_width, screen_height)
        # Find the coordinates from the center point(the player) to the top and bottom of the screen
        for drawx in range(playerx-screen_width//2, playerx+screen_width//2):
            if (drawx < 0):
                continue
            for drawy in range(playery-screen_height//2, playery+screen_height//2):
                if(drawy < 0):
                    continue
                if(fov_map[drawx-corner_x][drawy-corner_y] == False):
                    tcod.console_set_default_foreground(0, tcod.black)
                    tcod.console_put_char(0, drawx, drawy, ' ', tcod.BKGND_NONE)
                    if(abs(drawx-playerx) <=5) and (abs(drawy-playery) <= 5):
                        print(f"---\nCan't see: {drawx}, {drawy}\nPlayer:{playerx}, {playery}")
                    continue
                #If an object is there, draw it.
                #TODO: Make walls hide objects maybe???
                if self.objdict.get((playerz,drawx,drawy)):
                        #TODO: Find a better way to pick what to draw
                        self.objdict[(playerz, drawx, drawy)][-1].draw(corner_x, corner_y)
                else:
                    #Try Catch for drawing stuff outside the area
                    #TODO: Better handling for stuff not in this structure
                    try:
                        #Draw the tile
                        tile = self.tileset[self.map[playerz][drawx][drawy]]
                        tile.z = playerz
                        tile.x = drawx
                        tile.y = drawy
                        tile.draw(corner_x, corner_y)
                    except IndexError:
                        #Draw blank space if nothing is expected there
                        tcod.console_set_default_foreground(0, tcod.white)
                        tcod.console_put_char(0, drawx, drawy, ' ', tcod.BKGND_NONE)
