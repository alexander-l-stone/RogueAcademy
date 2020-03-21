from source.entity.drawableEntity import DrawableEntity
from source.entity.component.moveable import Moveable
from source.action.move_action import MoveAction

class Character(DrawableEntity):
    def __init__(self, z:int, x:int, y:int, char:str, color:tuple, *components):
        moveable:Moveable = Moveable(1)
        #TODO:Calculate vision_radius somehow
        self.vision_radius = 8
        DrawableEntity.__init__(self, z, x, y, char, color, moveable, 'blocks_movement', *components)
    
    def can_move(self, dz:int, dx:int, dy:int, area):
        """
        Check if a character can move somewhere
        """
        return self.get(Moveable).can_move(self, area, dz, dx, dy)
    
    def move(self, dz:int, dx:int, dy:int, area):
        """
        Makes a character move
        """
        return self.get(Moveable).move(self, area, dz, dx, dy)

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