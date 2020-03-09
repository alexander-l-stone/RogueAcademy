from source.entity.drawableEntity import DrawableEntity

class Area:
    def __init__(self, x: int, y: int, z: int, wall: DrawableEntity = DrawableEntity(-1, -1, -1, '#', (80, 80, 80), 'blocks_movement'), floor: DrawableEntity = DrawableEntity(-1, -1, -1, '.', (80, 80, 80))):
        self.x:int = x
        self.y:int = y
        self.z:int = z
        self.wall = wall
        self.floor = floor
        self.objdict = {}
    
    def draw(self, playerx, playery, playerz, screen_width, screen_height):
        for drawx in range(playerx-screen_width//2, playerx+screen_width//2):
            for drawy in range(playery-screen_height//2, playery+screen_height//2):
                if (self.objdict.get((drawx, drawy, playerz))):
                    self.objdict[(drawx, drawy, playerz)].draw(playerx-screen_width//2, playery-screen_height//2)

