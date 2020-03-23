import numpy
import tcod

from typing import List
from source.entity.drawableEntity import DrawableEntity

class Area:
    def __init__(self, z_length: int, x_length: int, y_length: int, tileset:dict = {1: DrawableEntity(-1, -1, -1, '.', (100,100,100)), 0: DrawableEntity(-1, -1, -1, '#', (100,100,100), 'blocks_movement')}):
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
        # 0 means occluded, positive means visisble
        self.fov_map = numpy.array([[[0 for y in range(self.y_length)] for x in range(self.x_length)] for z in range(self.z_length)])

    def compute_fov(self, z, x, y, radius):
        return tcod.map.compute_fov(self.fov_map[z], (x, y), radius=radius, algorithm=tcod.constants.FOV_SHADOW)

    def add_object(self, entity:DrawableEntity) -> None:
        """
        Adds an entity to a square.
        """
        if(entity.has("blocks_vision")):
            self.fov_map[entity.z, entity.x, entity.y] = 0

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
            if(entity.has("blocks_vision")):
                self.fov_map[entity.z, entity.x, entity.y] = 1
                for thing in entity_list:
                    if thing.has("blocks_vision"):
                        self.fov_map[entity.z, entity.x, entity.y] = 0
                        break
            if len(entity_list) == 0:
                del self.objdict[(entity.z, entity.x, entity.y)]
            return True
        else:
            return False
        

    def draw(self, playerz, playerx, playery, screen_width, screen_height, vision_radius, **kwargs) -> None:
        corner_x = playerx-screen_width//2
        corner_y = playery-screen_height//2
        #Check Field of view
        fov = self.compute_fov(playerz, playerx, playery, vision_radius)
        # Find the coordinates from the center point(the player) to the top and bottom of the screen
        for drawx in range(playerx-screen_width//2, playerx+screen_width//2):
            if(drawx < 0 or drawx > self.x_length-1):
                continue
            for drawy in range(playery-screen_height//2, playery+screen_height//2):
                if(drawy < 0 or drawy > self.y_length-1):
                    continue
                #If an object is there, draw it.
                if(fov[drawx, drawy]):
                    tcod.console_set_default_background(0, tcod.black)
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
                            if ("flag" in kwargs and kwargs["flag"] == "debug"):
                                tile.draw(corner_x, corner_y, override_color=(255, 0, 0))
                            else:
                                tile.draw(corner_x, corner_y)
                        except IndexError:
                            #Draw blank space if nothing is expected there
                            tcod.console_set_default_foreground(0, tcod.black)
                            tcod.console_put_char(0, drawx, drawy, ' ', tcod.BKGND_NONE)
                else:
                    #TODO: Maybe move the debug code around?
                    if ("flag" in kwargs and kwargs["flag"] == "debug"):
                        tcod.console_set_default_background(0, tcod.black)
                        if self.objdict.get((playerz, drawx, drawy)):
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
                                tcod.console_set_default_foreground(0, tcod.black)
                                tcod.console_put_char(0, drawx, drawy, ' ', tcod.BKGND_NONE)
