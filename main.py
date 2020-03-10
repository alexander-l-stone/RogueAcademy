import tcod
import tcod.event

from source.entity.drawableEntity import DrawableEntity
from source.area.area import Area

# Setup the font.
tcod.console_set_custom_font(
    "arial12x12.png",
    tcod.FONT_LAYOUT_TCOD | tcod.FONT_TYPE_GREYSCALE,)

#test object
player_entity = DrawableEntity(0, 24, 24, '@', (255, 255, 255))
SCREEN_HEIGHT = 50
SCREEN_WIDTH = 50

area = Area(2,100,100)

for x in range(area.x_length):
    for y in range(area.y_length):
        if (x+1)%5 == 0 or (y+1)%5 == 0:
            area.map[0,x,y] = False

area.objdict[(player_entity.z, player_entity.x, player_entity.y)] = player_entity
for x in range(player_entity.x-5, player_entity.x-4):
    for y in range(player_entity.y-5, player_entity.y-4):
        area.objdict[(player_entity.z, x, y)] = DrawableEntity(player_entity.z, x, y, 'K', (x*5,abs(x*10 - y*10),y*5))

# Initialize the root console in a context.
with tcod.console_init_root(SCREEN_HEIGHT, SCREEN_WIDTH, order="F", vsync=False) as root_console:
    while True:
        area.draw(player_entity.z, player_entity.x, player_entity.y, SCREEN_WIDTH, SCREEN_HEIGHT)
        tcod.console_flush()  # Show the console.
        for event in tcod.event.wait():
            if event.type == "QUIT":
                raise SystemExit()
    # The libtcod window will be closed at the end of this with-block.
