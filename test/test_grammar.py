import pytest
from source.grammar.GrammarRule import GrammarRule
from source.grammar.GrammarRule import GrammarVariable
from source.grammar.GrammarRule import GrammarVisualizer
from source.entity.entity import Entity

def test_can_instantiate_rule():
    """
        Ensure that GrammarRule can be instantiated and is its own type
    """
    assert GrammarRule
    rule = GrammarRule()
    assert GrammarRule is type(rule)

def test_can_instantiate_rule_with_args():
    """
        Ensure that GrammarRule can be instantiated with arguments.
    """
    selections = [["a"],["b"]]
    rule = GrammarRule("rule", selections)
    assert selections == rule.selections

def test_can_generate_rule():
    """
        Ensure that rules can be generated.
        Ensure that if a selection has multiple elements, they appear in order.
        Randomness is lightly tested with multiple generations.
    """
    selections = [["a"],["b"]]
    rule = GrammarRule("rule", selections)
    for i in range(10):
        result = GrammarRule.generate(rule)
        assert selections[0] == result or selections[1] == result
        assert selections[0] is not result
        assert selections[1] is not result

    selections = [["a","c"],["b","d"]]
    rule = GrammarRule("rule", selections)
    for i in range(10):
        result = GrammarRule.generate(rule)
        assert selections[0] == result or selections[1] == result
        assert selections[0] is not result
        assert selections[1] is not result

def test_can_generate_recursive():
    """
        Ensure that a rule internal to a rule is expanded during generation.
    """
    rule_leaf = GrammarRule("leaf", [["text"]])
    rule_branch = GrammarRule("branch", [[rule_leaf]])
    rule_root = GrammarRule("root", [[rule_branch]])
    result = GrammarRule.generate(rule_root)
    assert ["text"] == result

def test_variable():
    """
        Ensure that a variable can be instantiated.
        Ensure that it reports equal to strings equal to its name, and it hashes as that string.
    """
    var1 = GrammarVariable("var1")
    str1 = "var1"
    assert var1 == str1
    assert var1.__hash__() == str1.__hash__()

def test_use_variable():
    """
        GrammarRule.generate():
            Ensure that invocation of an undefined variable raises an error.
            Ensure that invocation of a defined variable populates the value.
    """
    str_varname = "var_1"
    str_value = "populate"
    rule_assign = GrammarRule("label_assign", [[str_value]], str_varname)
    var_recall_bad = GrammarVariable("var_garbage")
    root = GrammarRule("label_root", [[rule_assign, var_recall_bad]])
    try:
        result = GrammarRule.generate(root)
        assert False
    except ValueError:
        assert True

    var_recall_good = GrammarVariable(str_varname)
    root = GrammarRule("label_root", [[rule_assign, var_recall_good]])
    result = GrammarRule.generate(root)
    assert str_varname == var_recall_good
    assert [str_value] == result

def test_use_variable_multi_retains_identity():
    """
        Ensure that multiple invocations of the same variable retain pointer equality.
        Ensure that the populated variable is not the object in the rule tree.
            (rules should be immutable)
    """
    entity = Entity()
    entity2 = Entity()
    assert entity is not entity2
    rule_assign = GrammarRule("label_assign", [[entity]], "var1")
    var_1 = GrammarVariable("var1")
    root = GrammarRule("label_root", [[rule_assign, var_1, var_1]])
    result = GrammarRule.generate(root)
    assert entity is not result[0]
    assert entity is not result[1]
    assert result[0] is result[1]

def test_clone_variable_unique():
    """
        Clone flag on a GrammarVariable should cause the reference population to be cloned.
        Clones should be pointer-unique to all other populations of that value.
    """
    entity = Entity()
    entity2 = Entity()
    assert entity is not entity2
    rule_assign = GrammarRule("label_assign", [[entity]], "var1")
    var_1 = GrammarVariable("var1")
    var_1_clone = GrammarVariable("var1", True)
    root = GrammarRule("label_root", [[rule_assign, var_1, var_1_clone, var_1_clone, var_1]])
    result = GrammarRule.generate(root)
    assert entity is not result[0]
    assert entity is not result[1]
    assert entity is not result[2]
    assert entity is not result[3]
    assert result[0] is not result[1]
    assert result[0] is not result[2]
    assert result[0] is result[3] # these are both var_1, not cloned, should match
    assert result[1] is not result[2]
    assert result[1] is not result[3]
    assert result[2] is not result[3]

def test_internal_var():
    """
        Ensure that a variable can be invoked from within a later variable definition.
            (ensure that the variables dict is being passed successfully)
        Ensure that a variable defined within a variable definition can be called later scopelessly.
            (ensure that the variables dict is being passed by reference and successfully mutated)
    """
    # Could have assigned the vars to local variables but wanted to test that
    # creating multiple GrammarVariables works, not that there is a reason it would not.
    # Admittedly this is much less readable.
    rule_assign2 = GrammarRule("label_assign2", [["cod", GrammarVariable("var0")]], "var2")
    rule_assign1 = GrammarRule("label_assign1", [[rule_assign2, GrammarVariable("var2")]], "var1")
    rule_assign0 = GrammarRule("label_assign0", [["dog"]], "var0")
    rule_root = GrammarRule("label_root", [[rule_assign0, rule_assign1, GrammarVariable("var1"), GrammarVariable("var2")]]) 
    result = GrammarRule.generate(rule_root)
    assert ["cod", "dog", "cod", "dog"] == result

def test_process():
    """
    Expand a rule with a process function
    """
    rule = GrammarRule("label_rule", [[]], None, lambda sel : "Success")
    output = GrammarRule.generate(rule)
    assert ["Success"] == output

def test_process_gets_args():
    """
    Use the selection in a process lambda.
    Ensure that selection is expanded before being passed in.
    """
    rule_child = GrammarRule("label_child", [["Great"]])
    rule = GrammarRule("label_rule", [[rule_child]], None, lambda sel : f"{sel[0]} Success")
    output = GrammarRule.generate(rule)
    assert ["Great Success"] == output

def test_process_expansion():
    """
    Expand a rule with a process function which returns expandables.
    Ensure the function output is expanded and order is retained.
    """
    rule_child = GrammarRule("label_child", [["Success"]])
    rule_processor = GrammarRule("label_processor", [[]], None, lambda sel : rule_child)
    rule_root = GrammarRule("label_root", [[rule_processor]])
    output = GrammarRule.generate(rule_root)
    assert ["Success"] == output

    rule_child = GrammarRule("label_child", [["Success"]])
    rule_processor = GrammarRule("label_processor", [[]], None, lambda sel : ["Great", rule_child])
    rule_root = GrammarRule("label_root", [[rule_processor]], )
    output = GrammarRule.generate(rule_root)
    assert ["Great", "Success"] == output

def test_visualize():
    """
    Parses a sample syntax to output.
    Tests against a hardcoded sample output.
    """
    rule_assign2 = GrammarRule("label_assign2", [["cod", GrammarVariable("var0")]], "var2")
    rule_assign1 = GrammarRule("label_assign1", [[rule_assign2, GrammarVariable("var2")], [rule_assign2, GrammarVariable("var2"), GrammarVariable("var1")]], "var1")
    rule_assign0 = GrammarRule("label_assign0", [["dog"]], "var0")
    rule_root = GrammarRule("label_root", [[rule_assign0, rule_assign1, GrammarVariable("var1"), GrammarVariable("var2")]]) 
    visual = GrammarVisualizer.visualize(rule_root)
    print(f'{visual}')
    # set this to False to get the print to work so you can copy+paste
    # to http://mshang.ca/syntree/ 
    assert visual == "[label_root(Rule) [Selection [label_assign0(Rule) [Selection [Data dog]]][label_assign1(Rule) [Selection [label_assign2(Rule) [Selection [Data cod][Var var0]]][Var var2][Var var1]][Selection [label_assign2(Rule) [Selection [Data cod][Var var0]]][Var var2]]][Var var1][Var var2]]]"