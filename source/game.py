import tcod
import tcod.event
import random
from typing import Dict

from source.area.area import Area
from source.handlers.inputHandler import InputHandler
from source.entity.entity import Entity
from source.entity.player import Player
from source.action.action_queue import ActionQueue
from source.ui.ui_panel import UIPanel

from source.grammar.school.school_generator import SchoolGenerator

class Game:
    def __init__(self, config:Dict={}):
        self.config = config
        #setup font
        tcod.console_set_custom_font("terminal8x12_gs_ro.png", tcod.FONT_LAYOUT_ASCII_INROW | tcod.FONT_TYPE_GREYSCALE,)
        tileset = {
                    0: Entity(-1, -1, -1, '#', (100, 100, 100), flags={'blocks_movement':True, 'blocks_vision':True}),
                    1: Entity(-1, -1, -1, '.', (100, 100, 100), {}),
                    2: Entity(-1, -1, -1, '#', (0, 0, 255), flags={'blocks_movement': True, 'blocks_vision': True}),
                    3: Entity(-1, -1, -1, '.', (0, 0, 255), {}),
                    4: Entity(-1, -1, -1, '#', (180, 180, 180), flags={'blocks_movement': True, 'blocks_vision': True}),
                    5: Entity(-1, -1, -1, '.', (180, 180, 180), {}),
                    }
        self.curr_area:Area = Area(2, 200, 200, tileset=tileset)
        self.SCREEN_WIDTH:int = 50
        self.SCREEN_HEIGHT:int = 50
        self.InputHandler:InputHandler = InputHandler()
        self.player:Player = Player(0, 24, 24, '@', (255, 255, 255))
        self.global_queue = ActionQueue()
        self.global_time = 0
        #TODO: Figure out panel heights for this
        self.bot_ui = UIPanel(0, self.SCREEN_HEIGHT - 5, 5, self.SCREEN_WIDTH)
        self.top_ui = UIPanel(0, 0, 5, self.SCREEN_WIDTH)
    
    def generate_school(self) -> None:
        """
            This function will randomly generate the school
        """
        rooms = SchoolGenerator.generate_school(self.curr_area)
        self.player.x = random.randint(rooms[0].x1+1, rooms[0].x2)
        self.player.y = random.randint(rooms[0].y1+1, rooms[0].y2)
        self.curr_area.add_object(self.player)

    def render(self) -> None:
        self.curr_area.draw(self.player.z, self.player.x,self.player.y, self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.player.vision_radius, **self.config)
        self.bot_ui.draw()
        self.bot_ui.print_string(1, 1, f"({self.player.z}, {self.player.x}, {self.curr_area.y_length - self.player.y})")
        self.top_ui.draw()
        self.top_ui.print_string(1, 1, f"{self.global_time}")
        tcod.console_flush()  # Show the console.

    def game_loop(self) -> None:
        with tcod.console_init_root(self.SCREEN_HEIGHT, self.SCREEN_WIDTH, order="F", vsync=False) as root_console:
            root_console.clear()
            self.render()
            while not tcod.console_is_window_closed():
                if self.global_queue.player_actions_count > 0:
                    self.global_queue.resolve_actions(self.global_time)
                    self.global_time += 1
                    root_console.clear()
                    self.render()
                else:
                    for event in tcod.event.wait():
                        if event.type == "KEYDOWN":
                            result = self.InputHandler.handle_keypress(event)
                            if(result["type"] == "move"):
                                self.player.move_action(result["value"][0], result["value"][1], result["value"][2], self.curr_area, self.global_queue)
                        if event.type == "QUIT":
                            raise SystemExit()
