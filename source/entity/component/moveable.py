class Moveable:
    def __init__(self, speed:float):
        #TODO: Use speed to add this move to the global action queue
        self.speed:float = speed
    
    def can_move(self, entity, area, dz, dx, dy):
        """
        Check if I can move the entity the given delta.

        Return true if possible, false if not possible.
        """
        entity_list = area.objdict.get((entity.z+dz, entity.x+dx, entity.y+dy))
        if (entity_list):
            for obj in entity_list:
                if obj.has("blocks_movement"):
                    return False
            return True
        else:
            try:
                if (area.tileset[area.map[entity.z+dz, entity.x+dx, entity.y+dy]].has('blocks_movement')):
                    return False
                else:
                    return True
            except IndexError:
                return False
    
    def move(self, entity, area, dz, dx, dy) -> None:
        area.remove_object(entity)
        entity.z += dz
        entity.x += dx
        entity.y += dy
        area.add_object(entity)

