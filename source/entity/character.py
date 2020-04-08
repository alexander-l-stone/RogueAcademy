from source.entity.entity import Entity
from source.action.move_action import MoveAction

class Character(Entity):
    def __init__(self, z:int, x:int, y:int, char:str, color:tuple, flags:dict={}, **kwargs:dict):
        #TODO:Calculate vision_radius somehow
        self.vision_radius:int = 12
        Entity.__init__(self, z, x, y, char, color, flags)
        self.flags['blocks_movement'] = True
    
    def can_move(self, dz:int, dx:int, dy:int, area):
        """
        Check if a character can move somewhere
        """
        entity_list = area.objdict.get((self.z+dz, self.x+dx, self.y+dy))
        if (entity_list):
            for obj in entity_list:
                if 'blocks_movement' in obj.flags:
                    return False
            return True
        else:
            try:
                z_attempt = self.z + dz
                if (z_attempt < 0) or (z_attempt > area.z_length - 1):
                    return False
                x_attempt = self.x + dx
                if (x_attempt < 0) or (x_attempt > area.x_length - 1):
                    return False
                y_attempt = self.y + dy
                if(y_attempt < 0) or (y_attempt > area.y_length - 1):
                    return False
                if ('blocks_movement' in area.tileset[area.map[z_attempt, x_attempt, y_attempt]].flags):
                    return False
                else:
                    return True
            except IndexError:
                return False
    
    def move(self, dz:int, dx:int, dy:int, area):
        """
        Makes a character move
        """
        area.remove_object(self)
        self.z += dz
        self.x += dx
        self.y += dy
        area.add_object(self)

    #TODO: Rename this to something better
    def move_action(self, dz:int, dx:int, dy:int, area, queue):
        """
        Generates a move action for this character
        """
        if self.can_move(dz, dx, dy, area):
            move_action:MoveAction = MoveAction( self, 1, area, dz, dx, dy)
            queue.push(move_action)
            return True
        else:
            return False
