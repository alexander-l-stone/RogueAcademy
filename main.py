import tcod
import tcod.event

from source.entity.drawableEntity import DrawableEntity
from source.area.area import Area

# Setup the font.
tcod.console_set_custom_font(
    "arial12x12.png",
    tcod.FONT_LAYOUT_TCOD | tcod.FONT_TYPE_GREYSCALE,)

#test object
player_entity = DrawableEntity(0, 25, 25, '@', (255, 255, 255))
SCREEN_HEIGHT = 50
SCREEN_WIDTH = 50

area = Area(2,20,20)

for x in range(area.x_length):
    for y in range(area.y_length):
        if (x+1)%5 == 0 or (y+1)%5 == 0:
            area.map[0,x,y] = False

area.objdict[(player_entity.z, player_entity.x, player_entity.y)] = player_entity
area.objdict[(player_entity.z, player_entity.x-10, player_entity.y-10)] = DrawableEntity(player_entity.z, player_entity.x-5, player_entity.y-5, 'K', (0,255,0))

# Initialize the root console in a context.
with tcod.console_init_root(SCREEN_HEIGHT, SCREEN_WIDTH, order="F") as root_console:
    while True:
        area.draw(player_entity.z, player_entity.x, player_entity.y, SCREEN_WIDTH, SCREEN_HEIGHT)
        tcod.console_flush()  # Show the console.
        for event in tcod.event.wait():
            if event.type == "QUIT":
                raise SystemExit()
    # The libtcod window will be closed at the end of this with-block.
