from source.grammar.GrammarRule import GrammarRule, GrammarVariable
from source.area.area import Area

class SchoolGenerator:
    """
    Randomly generates a school
    """
    def __init__(self, length:int, width:int, height:int = 1):
        self.length:int = length
        self.width:int = width
        self.height:int = height
        #This is in z, x, y order
        self.area = Area(self.height, self.length, self.width)
