import tcod
import tcod.event
import argparse

from source.game import Game
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--debug", required=False, action='store_true')
    config = vars(ap.parse_args())

    game = Game(config)
    game.generate_school()

    # Initialize the root console in a context.
    game.game_loop()
    # The libtcod window will be closed at the end of this with-block.
