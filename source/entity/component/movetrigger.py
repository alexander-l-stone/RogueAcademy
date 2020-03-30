from typing import Callable
from source.entity.entity import Entity

class MoveTrigger:
    def __init__(self, react:Callable[[Entity],None]):
        self.react:Callable[[Entity],None] = react
