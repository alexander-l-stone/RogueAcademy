import tcod
import tcod.event

from source.area.area import Area
from source.handlers.inputHandler import InputHandler
from source.entity.drawableEntity import DrawableEntity
from source.entity.player import Player
from source.action.action_queue import ActionQueue

class Game:
    def __init__(self):
        #setup font
        tcod.console_set_custom_font("arial12x12.png", tcod.FONT_LAYOUT_TCOD | tcod.FONT_TYPE_GREYSCALE,)
        self.curr_area:Area = Area(2, 100, 100)
        self.SCREEN_WIDTH:int = 50
        self.SCREEN_HEIGHT:int = 50
        self.InputHandler:InputHandler = InputHandler()
        self.player:Player = Player(0, 24, 24, '@', (255, 255, 255))
        self.global_queue = ActionQueue()
    
    def generate_school(self):
        """
            This function will randomly generate the school
        """
        for x in range(self.curr_area.x_length):
            for y in range(self.curr_area.y_length):
                if (x+1) % 5 == 0 or (y+1) % 5 == 0:
                    self.curr_area.map[0, x, y] = False
        self.curr_area.add_object(self.player)
        for x in range(self.player.x-5, self.player.x-4):
            for y in range(self.player.y-5, self.player.y-4):
                self.curr_area.add_object(DrawableEntity(self.player.z, x, y, 'K', (x*5, abs(x*10 - y*10), y*5)))

    def render(self):
        self.curr_area.draw(self.player.z, self.player.x,self.player.y, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        tcod.console_flush()  # Show the console.
    
    def game_loop(self):
        with tcod.console_init_root(self.SCREEN_HEIGHT, self.SCREEN_WIDTH, order="F", vsync=False) as root_console:
            while not tcod.console_is_window_closed():
                root_console.clear()
                self.render()
                if self.global_queue.player_actions_count > 0:
                    self.global_queue.pop()
                else:
                    for event in tcod.event.wait():
                        if event.type == "KEYDOWN":
                            result = self.InputHandler.handle_keypress(event)
                            if(result["type"] == "move"):
                                self.player.move_action(result["value"][0], result["value"][1], result["value"][2], self.curr_area, self.global_queue)
                        if event.type == "QUIT":
                            raise SystemExit()
