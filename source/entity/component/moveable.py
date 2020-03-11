class Moveable:
    def __init__(self, speed:float):
        #TODO: Use speed to add this move to the global action queue
        self.speed:float = speed
    
    def attempt_move(self, entity, area, dz, dx, dy):
        """
            Check if I can move to the entity the given delta.

            Return true if possible, false if not possible.
        """
        if (area.objdict.get((entity.z+dz, entity.x+dx, entity.y+dy))):
            for obj in area.objdict[(entity.z+dz, entity.x+dx, entity.y+dy)]:
                if obj.has("blocks_movement"):
                    return False
            return True
        else:
            try:
                if (area.map[entity.z+dz, entity.x+dx, entity.y+dy]):
                    return False
                else:
                    return True
            except IndexError:
                return False
    
    def move(self, entity, area, dz, dx, dy):
        area.remove_object(entity)
        entity.z += dz
        entity.x += dx
        entity.y += dy
        area.add_object(entity)

