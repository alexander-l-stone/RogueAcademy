from typing import List

class GrammarRule:

    def __init__(self, parent:GrammarRule=None, selections:List[List]=[]):
        self.parent:GrammarRule = parent # rule
        self.selections:List[List] = selections # list rule or typestring
