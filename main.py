import tcod
import tcod.event

from source.game import Game


if __name__ == '__main__':
    #Make a Game
    game = Game()
    #Generate a School
    game.generate_school()
    #Run the game
    game.game_loop()
