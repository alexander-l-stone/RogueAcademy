from source.grammar.GrammarRule import GrammarRule
import random

class Grammar:

    def __init__(self, *components):
        self.components = {}

        self.typemap = {} # string :: List[object] 
        self.root = None # rule

    def generate(self, rule:GrammarRule=None):
        if rule == None:
            rule = self.root

        arr = [rule]

        for i,r in enumerate(arr):
            if r is not GrammarRule:
                continue
            # pop the rule
            arr.remove(i)
            # pick an option for this symbol
            num = random.randrange(0, len(rule.selections))
            selection = rule.selections[num]
            # add the chosen selection
            # go from the back so they end up in order
            for child in selection.reversed():
                arr.insert(i, child)

        return arr