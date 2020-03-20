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
                z_attempt = entity.z + dz
                if (z_attempt < 0) or (z_attempt > area.z_length - 1):
                    return False
                x_attempt = entity.x + dx
                if (x_attempt < 0) or (x_attempt > area.x_length - 1):
                    return False
                y_attempt = entity.y + dy
                if(y_attempt < 0) or (y_attempt > area.y_length - 1):
                    return False
                if (area.tileset[area.map[z_attempt, x_attempt, y_attempt]].has('blocks_movement')):
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

