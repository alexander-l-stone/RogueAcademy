from source.action.action import Action
from source.area.area import Area
from source.entity.entity import Entity

class MoveAction(Action):
    def __init__(self, originator:Entity, time_remaining:int, area:Area, dz:int, dx:int, dy:int):
        Action.__init__(self, originator, time_remaining)
        self.area = area
        self.dz = dz
        self.dx = dx
        self.dy = dy

    def resolve_action(self):
        """
            Override resolve to make the character move
        """
        if (self.originator.can_move(self.dz, self.dx, self.dy, self.area)):
            return self.originator.move(self.dz, self.dx, self.dy, self.area)
        else:
            return False