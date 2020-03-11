from typing import List,Dict
import random
import copy

class GrammarRule:

    # TODO consider adding function hooks to rules for self-population

    def __init__(self, selections:List[List]=[], assignVar:str=None):
        """
            Will expand to one of the selection sublists, each element of which will be
            recursively expanded (if rules or variables) and added to the grammar output in-order. A raw value
            (anything not GrammarRule or GrammarVariable) will be deepcopied so the rule can be reused.
            
            If assignVar is present, INSTEAD of outputting, the chosen selection will be fully expanded and
            the result stored for the remainder of generation (see generate()). Any GrammarVariables with the
            same name string will import that value by pointer.
            IMPORTANT: THE VALUE WILL NOT OUTPUT IF IT IS ASSIGNED!
            If you want the rule to output as well, include a GrammarVariable of the same name immediately after the assigning rule.

            selections -- A list of lists of elements (GrammarRule, GrammarVariable, raw values) 
            assignVar -- A string or None. If not None, assigns the result to a variable of this name instead of outputting values.
        """
        self.selections:List[List] = selections # list rule or typestring
        self.assignVar = assignVar

    @staticmethod
    def generate(root): # must be type GrammarRule; can't use typing because GrammarRule is not yet defined
        """
            Expands the given rule recursively. If a rule has assignVariable set, instead of outputting it will
            store its output in a variable which persists until the end of generation. There is no scoping, but the
            rule tree is parsed in-order, so variables cannot be successfully invoked until the assigning rule node is parsed.
            A variable may be assigned to multiple times, overwriting the previous value. Previously parsed variables will retain
            whatever value existed in the variable at the time they were parsed.

            If a GrammarVariable appears, it will be populated with the contents of the variable of the same name
            (i.e. matching the assignVar value of a previously executed rule). They are populated by pointer, and have "is" equality
            to other populations of identically named GrammarVariables.

            Attempting to invoke a variable which is not defined will throw an error.

            All values (including variable values) are deepcopied, so the original GrammarRules, GrammarVariables, and other values
            in the rule tree remain immutable and the rule can be safely reused for future generation.
        """
        if root == None or type(root) is not GrammarRule:
            return None
        return GrammarRule._expandRule([root], {})

    @staticmethod
    def _expandRule(stack:List, variables:Dict):
        output:List = []

        while len(stack) > 0:
            # pop the element
            elem = stack.pop()

            if type(elem) is GrammarRule:
                # pick an option for this symbol
                rand = random.randrange(0, len(elem.selections))
                selection = elem.selections[rand]
                # assign to a variable if necessary
                if elem.assignVar:
                    variables[elem.assignVar] = copy.deepcopy(GrammarRule._expandRule(selection[::-1], variables))
                else:
                    # add the chosen selection
                    # go from the back so they end up in order
                    for child in selection[::-1]:
                        stack.append(child)
            elif type(elem) is GrammarVariable:
                # add the variable's value(s) directly to output (they've already been copied)
                value = variables.get(elem)
                if value:
                    for child in value:
                        output.append(child)
                else:
                    raise ValueError(f"Variable {elem} not found")
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
    
    def __hash__(self):
        return self.name.__hash__()
