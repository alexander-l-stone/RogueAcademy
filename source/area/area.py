import numpy
import tcod

from typing import List, Dict
from source.entity.entity import Entity

default_tileset = {
                    0: Entity(-1, -1, -1, '#', (100, 100, 100), flags={'blocks_movement': True}),
                    1: Entity(-1, -1, -1, '.', (100, 100, 100)),
                    }
class Area:
    def __init__(self, z_length:int, x_length:int, y_length:int, tileset:dict = default_tileset):
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
        self.explored_map = numpy.array([[[False for y in range(self.y_length)] for x in range(self.x_length)] for z in range(self.z_length)])

    def compute_fov(self, z, x, y, radius):
        return tcod.map.compute_fov(self.fov_map[z], (x, y), radius=radius, algorithm=tcod.constants.FOV_SHADOW)

    def add_object(self, entity:Entity) -> None:
        """
        Adds an entity to a square.
        """
        if("blocks_vision" in entity.flags):
            self.fov_map[entity.z, entity.x, entity.y] = 0

        if (self.objdict.get((entity.z, entity.x, entity.y))):
            self.objdict[(entity.z, entity.x, entity.y)].append(entity)
        else:
            self.objdict[(entity.z, entity.x, entity.y)] = [entity]
    
    def get_object(self, z:int, x:int, y:int) -> List[Entity]:
        """
        Gets the list of entities at the given coordinates
        """
        return self.objdict.get((z, x, y))
    
    def remove_object(self,entity:Entity) -> bool:
        """
        Removes an entity from objdict

        Returns true if it was removed, false otherwise
        """
        entity_list = self.objdict.get((entity.z, entity.x, entity.y))
        if (entity in entity_list):
            entity_list.remove(entity)
            if("blocks_vision" in entity.flags):
                self.fov_map[entity.z, entity.x, entity.y] = 1
                for thing in entity_list:
                    if "blocks_vision" in thing.flags:
                        self.fov_map[entity.z, entity.x, entity.y] = 0
                        break
            if len(entity_list) == 0:
                del self.objdict[(entity.z, entity.x, entity.y)]
            return True
        else:
            return False
        

    def draw(self, playerz, playerx, playery, screen_width, screen_height, vision_radius, **config) -> None:
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
                if(fov[drawx, drawy] or ("debug" in config and config["debug"])):
                    self.explored_map[playerz, drawx, drawy] = True
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
                            if (fov[drawx, drawy] and "debug" in config and config["debug"]):
                                tile.draw(corner_x, corner_y, override_color=(255,0,0))
                            else:
                                tile.draw(corner_x, corner_y)
                        except IndexError:
                            #Draw blank space if nothing is expected there
                            tcod.console_set_default_foreground(0, tcod.black)
                            tcod.console_put_char(0, drawx, drawy, ' ', tcod.BKGND_NONE)
                elif(self.explored_map[playerz, drawx, drawy]):
                    if self.objdict.get((playerz, drawx, drawy)):
                        #TODO: Find a better way to pick what to draw
                        self.objdict[(playerz, drawx, drawy)][-1].explored_draw(corner_x, corner_y)
                    else:
                        #Try Catch for drawing stuff outside the area
                        #TODO: Better handling for stuff not in this structure
                        try:
                            #Draw the tile
                            tile = self.tileset[self.map[playerz][drawx][drawy]]
                            tile.z = playerz
                            tile.x = drawx
                            tile.y = drawy
                            tile.explored_draw(corner_x, corner_y)
                        except IndexError:
                            #Draw blank space if nothing is expected there
                            tcod.console_set_default_foreground(0, tcod.black)
                            tcod.console_put_char(0, drawx, drawy, ' ', tcod.BKGND_NONE)
