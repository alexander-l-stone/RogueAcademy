import tcod
import tcod.event

from source.game import Game

# Setup the font.
tcod.console_set_custom_font(
    "arial12x12.png",
    tcod.FONT_LAYOUT_TCOD | tcod.FONT_TYPE_GREYSCALE,)

#test object

SCREEN_HEIGHT:int = 50
SCREEN_WIDTH:int = 50

game = Game()
game.generate_school()

# Initialize the root console in a context.
game.game_loop()
    # The libtcod window will be closed at the end of this with-block.
