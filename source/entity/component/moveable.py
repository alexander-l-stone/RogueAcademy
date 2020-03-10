class Moveable:
    def __init__(self, speed:float):
        #TODO: Use speed to add this move to the global action queue
        self.speed:float = speed
    
    def attempt_move(self, entity, area, dz, dx, dy):
        if (area.objdict.get((entity.z+dz, entity.x+dx, entity.y+dy))):
            if (area.objdict[(entity.z+dz, entity.x+dx, entity.y+dy)].has("blocks_movement")):
                return False
            elif (area.map[entity.z+dz, entity.x+dx, entity.y+dy]):
                return False
            else:
                return True
        else:
            if (area.map[entity.z+dz, entity.x+dx, entity.y+dy]):
                return False
            else:
                return True
    
    def move(self, entity, area, dz, dx, dy):
        area.objdict[entity.z, entity.x, entity.y] = None
        entity.z += dz
        entity.x += dx
        entity.y += dy
        area.objdict[entity.z, entity.x, entity.y] = entity

