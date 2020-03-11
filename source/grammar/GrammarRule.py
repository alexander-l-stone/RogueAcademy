from typing import List,Dict
import random
import copy

class GrammarRule:

    # TODO consider adding function hooks to rules for self-population

    def __init__(self, selections:List[List]=[], assignVar:str=None):
        self.selections:List[List] = selections # list rule or typestring
        self.assignVar = assignVar

    @staticmethod
    def generate(root): # must be type GrammarRule; can't use typing because GrammarRule is not yet defined
        if root == None or type(root) is not GrammarRule:
            return None
        stack:List = [root]
        output:List = []
        variables = {}    

        while len(stack) > 0:
            # pop the element
            elem = stack.pop()

            if type(elem) is GrammarRule:
                # pick an option for this symbol
                rand = random.randrange(0, len(elem.selections))
                selection = elem.selections[rand]
                # assign to a variable if necessary
                if elem.assignVar:
                    variables[elem.assignVar] = selection
                else:
                    # add the chosen selection
                    # go from the back so they end up in order
                    for child in selection[::-1]:
                        stack.append(child)
            elif type(elem) is GrammarVariable:
                # add the variable's value(s)
                # go from the back so they end up in order
                value = variables.get(elem)
                if value:
                    for child in value[::-1]:
                        stack.append(child)
                else:
                    stack.append(f"Variable {elem} not found")
            else:
                # copy the template object
                output.append(copy.deepcopy(elem))

        return output
    
    def __str__(self):
        return f"<{self.selections}, {self.assignVar}>"

class GrammarVariable:
    def __init__(self, name):
        self.name = name

    def __eq__(self,other):
        if other is GrammarVariable:
            return self.name == other.name
        return self.name == other

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name

    def __hash__(self):
        return self.name.__hash__()
