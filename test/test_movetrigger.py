import pytest

from source.area.area import Area
from source.entity.component.movetrigger import MoveTrigger
from source.entity.drawableEntity import DrawableEntity
from source.entity.component.moveable import Moveable
from source.entity.player import Player

def printThing(entity):
    msg:str = "It's a trap!"
    print(f"thing {entity}")

def test_does_trigger():
    safestr = "It's safe"
    trapstr = "It's a trap!"
    msg:str = safestr
    test_trigger = MoveTrigger(printThing)
    test_trap = DrawableEntity(0,0,0,'+',(0,255,0),test_trigger)
    tmp_area = Area(5,5,5)
    tmp_area.add_object(test_trap)

    test_player = Player(0,1,0,'@',(255,0,0))
    tmp_area.add_object(test_player)

    test_player.get(Moveable).move(test_player, tmp_area, 0, -1, 0)
    assert msg == False
