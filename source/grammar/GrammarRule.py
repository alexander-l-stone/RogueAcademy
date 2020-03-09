from typing import List,Dict
import random

class GrammarRule:

    def __init__(self, selections:List[List]=[]):
        self.selections:List[List] = selections # list rule or typestring

    @staticmethod
    def generate(rule:GrammarRule):
        if rule == None:
            return None
        arr:List = [rule]

        for i,r in enumerate(arr):
            # pop the rule
            arr.remove(i)
            # clone the template object
            if r is not GrammarRule:
                arr.insert(i,r.clone())
                continue
            # pick an option for this symbol
            rand = random.randrange(0, len(rule.selections))
            selection = rule.selections[rand]
            # add the chosen selection
            # go from the back so they end up in order
            for child in selection.reversed():
                arr.insert(i, child)

        return arr
