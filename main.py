import tcod
import tcod.event

from source.game import Game
if __name__ == "__main__":
    game = Game()
    game.generate_school()

    # Initialize the root console in a context.
    game.game_loop()
    # The libtcod window will be closed at the end of this with-block.
