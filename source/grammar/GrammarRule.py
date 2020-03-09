from typing import List

class GrammarRule:

    def __init__(self, *components):
        self.components = {}

        self.parent:GrammarRule = None # rule
        self.selections:List[List] = [] # list rule or typestring