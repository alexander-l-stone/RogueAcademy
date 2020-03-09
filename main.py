import tcod
import tcod.event

from source.entity.drawableEntity import DrawableEntity

# Setup the font.
tcod.console_set_custom_font(
    "arial12x12.png",
    tcod.FONT_LAYOUT_TCOD | tcod.FONT_TYPE_GREYSCALE,)

#test object
player_entity = DrawableEntity(30, 30, '@', (255, 255, 255))

# Initialize the root console in a context.
with tcod.console_init_root(80, 60, order="F") as root_console:
    root_console.print_(x=0, y=0, string='Hello World!')
    while True:
        player_entity.draw()
        tcod.console_flush()  # Show the console.
        for event in tcod.event.wait():
            if event.type == "QUIT":
                raise SystemExit()
    # The libtcod window will be closed at the end of this with-block.
