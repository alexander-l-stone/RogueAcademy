import random
from typing import List,Dict

from source.grammar.school.blueprint import Blueprint
from source.grammar.GrammarRule import GrammarRule, GrammarVariable

GRID_SIZE: int = 20

rule_room_size = GrammarRule("size", [[]], None, lambda sel : random.randint(max(3,GRID_SIZE-10),max(8,GRID_SIZE-5)))
rule_room_floor = GrammarRule("floor", [[1], [3]])
rule_room_wall = GrammarRule("wall", [[2]])
# z x y floorTile
rule_room = GrammarRule("room", [[1, rule_room_size, rule_room_size, rule_room_floor, rule_room_wall]], None, lambda sel: Rectangle.create(sel))

rule_room_type = GrammarRule("room_type", [["bathroom"], ["classroom"], ["storage_room"]])

class RoomGenerator:
    """
    Randomly generates a room
    """
    def __init__(self, room:Blueprint):
        self.room = room

    def generate_room(self) -> None:
        pass
