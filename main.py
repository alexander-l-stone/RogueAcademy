import tcod
import tcod.event

from source.entity.drawableEntity import DrawableEntity
from source.area.area import Area

# Setup the font.
tcod.console_set_custom_font(
    "arial12x12.png",
    tcod.FONT_LAYOUT_TCOD | tcod.FONT_TYPE_GREYSCALE,)

#test object
player_entity = DrawableEntity(0, 50, 50, '@', (255, 255, 255))
SCREEN_HEIGHT = 80
SCREEN_WIDTH = 60

area = Area(2,100,100)

area.objdict[(player_entity.x, player_entity.y, player_entity.z)] = player_entity

# Initialize the root console in a context.
with tcod.console_init_root(SCREEN_HEIGHT, SCREEN_WIDTH, order="F") as root_console:
    while True:
        area.draw(player_entity.x, player_entity.y, player_entity.z, SCREEN_WIDTH, SCREEN_HEIGHT)
        tcod.console_flush()  # Show the console.
        for event in tcod.event.wait():
            if event.type == "QUIT":
                raise SystemExit()
    # The libtcod window will be closed at the end of this with-block.
