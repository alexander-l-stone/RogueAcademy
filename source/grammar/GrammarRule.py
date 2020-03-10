from typing import List,Dict
import random
import copy

class GrammarRule:

    # TODO add code to store results as variables for use in the remainder of generation

    def __init__(self, selections:List[List]=[]):
        self.selections:List[List] = selections # list rule or typestring

    @staticmethod
    def generate(rule): #rule must be of type Grammar Rule
        if rule == None:
            return None
        arr:List = [rule]

        for i,r in enumerate(arr):
            # pop the rule
            arr.pop(i)
            # clone the template object
            if type(r) is not GrammarRule:
                arr.insert(i,copy.deepcopy(r))
                continue
            # pick an option for this symbol
            rand = random.randrange(0, len(rule.selections))
            selection = rule.selections[rand]
            # add the chosen selection
            # go from the back so they end up in order
            for child in selection[::-1]:
                arr.insert(i, child)

        return arr
