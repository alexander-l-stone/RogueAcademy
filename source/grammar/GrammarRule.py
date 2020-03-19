from typing import List,Dict,Any,Callable,Union
import random
import copy

class GrammarRule:

    # TODO consider adding function hooks to rules for self-population

    def __init__(self, selections:List[List]=[], label:str=None, assignVar:str=None, process:Callable[[list], Any]=None):
        """
        Will expand to one of the selection sublists, each element of which will be
        recursively expanded (if rules or variables) and added to the grammar output in-order. A raw value
        (anything not GrammarRule or GrammarVariable) will be deepcopied so the rule can be reused.
        
        If assignVar is present, INSTEAD of outputting, the chosen selection will be fully expanded and
        the result stored for the remainder of generation (see generate()). Any GrammarVariables with the
        same name string will import that value by pointer.
        IMPORTANT: THE VALUE WILL NOT OUTPUT IF IT IS ASSIGNED!
        If you want the rule to output as well, include a GrammarVariable of the same name immediately after the assigning rule.

        If process is present, after the output selection is generated the function in the process variable will
        be run on the generated selection, and its return value replaces the selection. This occurs regardless of
        the presence of assignVar, so the processed value will be the stored value if assignVar is present, and if
        not the processed value will be the output value.

        selections -- A list of lists of elements (GrammarRule, GrammarVariable, raw values) 
        label -- string name WITHOUT WHITESPACE used for debugging and visualization. Do not include whitespace in the label.
        assignVar -- A string or None. If not None, assigns the result to a variable of this name instead of outputting values.
        process -- A callable function or None. If not none, the function is run upon the generated selection, and its return value will replace the selection.
        """
        self.selections:List[List] = selections # list rule or typestring
        self.label:str = label
        self.assignVar:Union[str,None] = assignVar # string or None
        self.process:Union[None,Callable[[list], Any]] = process

    @staticmethod
    def generate(root) -> List: # GrammarRule or List
        """
        Expands the given rule recursively. If a rule has assignVariable set, instead of outputting it will
        store its output in a variable which persists until the end of generation. There is no scoping, but the
        rule tree is parsed in-order, so variables cannot be successfully invoked until the assigning rule node is parsed.
        A variable may be assigned to multiple times, overwriting the previous value. Previously parsed variables will retain
        whatever value existed in the variable at the time they were parsed.

        Rules with a process function set will run that function on their generated selection and use the output of that
        function in place of the generated selection, either to store in a variable or output as appropriate.

        If a GrammarVariable appears, it will be populated with the contents of the variable of the same name
        (i.e. matching the assignVar value of a previously executed rule). They are populated by pointer, and have "is" equality
        to other populations of identically named GrammarVariables. If the GrammarVariable has the property clone=True, the value
        will instead be deepcopied (again) before being added to output, and will not have pointer equality.

        Attempting to invoke a variable which is not defined will throw an error.

        All values (including variable values) are deepcopied, so the original GrammarRules, GrammarVariables, and other values
        in the rule tree remain immutable and the rule can be safely reused for future generation.
        """
        if root == None:
            return None
        return GrammarRule._expandRule([root], {})

    @staticmethod
    def _expandRule(stack:List, variables:Dict):
        output:List = []

        while len(stack) > 0:
            # debug prints for watching stack in realtime, do not delete
            """
            string = "["
            for s in output:
                string += str(s) + ", "
            if (len(string) > 2):
                string = string[0:-2] + "]"
            else:
                string += "]"
            print(f"\nOUTPUT {string}")
            string = "["
            for s in stack:
                string += str(s) + ", "
            if (len(string) > 2):
                string = string[0:-2] + "]"
            else:
                string += "]"
            print(f"STACK {string}")
            """
            # pop the element
            elem = stack.pop()
            #print(f"POP {elem}")

            if type(elem) is GrammarRule:
                # pick an option for this symbol
                rand = random.randrange(0, len(elem.selections))
                selection = elem.selections[rand]
                # assign to a variable if necessary
                if elem.assignVar:
                    variables[elem.assignVar] = copy.deepcopy(GrammarRule._expandRule(selection[::-1], variables))
                    if elem.process:
                        variables[elem.assignVar] = elem.process(variables[elem.assignVar])
                else:
                    if elem.process:
                        stack.append(elem.process(copy.deepcopy(GrammarRule._expandRule(selection[::-1], variables))))
                    else:
                        # add the chosen selection
                        # go from the back so they end up in order
                        for child in selection[::-1]:
                            #print(f"PUSH {child}")
                            stack.append(child)
            elif type(elem) is GrammarVariable:
                # add the variable's value(s) directly to output (they've already been copied)
                value = variables.get(elem)
                if value:
                    if elem.clone:
                        for child in value:
                            output.append(copy.deepcopy(child))
                    else:
                        for child in value:
                            output.append(child)
                else:
                    raise ValueError(f"Variable {elem} not found")
            else:
                # copy the template object
                output.append(copy.deepcopy(elem))

        return output
    
    def __str__(self):
        return f"<{self.selections}, {self.assignVar}, {self.process}>"

class GrammarVariable:
    """
    A variable reference to be used in GrammarRule trees. This node will be replaced with the
    value stored in the variable of the same name.

    name -- the variable to look up
    clone -- If True, the variable value will be deepcopied before it is added to the generation output
    """
    def __init__(self, name:str, clone:bool=False):
        self.name = name
        self.clone = clone

    def __eq__(self,other):
        if other is GrammarVariable:
            return self.name == other.name
        return self.name == other

    def __str__(self):
        return self.name
    
    def __hash__(self):
        return self.name.__hash__()

class GrammarVisualizer:

    def __init__(self, close:str):
        self.close = close

    @staticmethod
    def visualize(root) -> str:
        """
        Exports the rule in syntree format
        Paste the result in here
        http://mshang.ca/syntree/
        """
        stack:list = [root]
        output:str = ""
        while len(stack) > 0:
            elem = stack.pop()
            if type(elem) is GrammarRule:
                if elem.label:
                    output = f"{output}[{elem.label}(Rule) "
                else:
                    output = f"{output}[Rule "
                stack.append(GrammarVisualizer("]"))
                for sel in elem.selections:
                    stack.append(GrammarVisualizer(""))
                    for child in sel:
                        stack.append(child)
                    stack.append(GrammarVisualizer("[Selection "))
            elif type(elem) is GrammarVariable:
                output = f"{output}[Var {elem}]"
            elif type(elem) is GrammarVisualizer:
                output = f"{output}{elem.close}"
            else:
                output = f"{output}[Data {elem}]"
        return output

