import pytest
from source.grammar.GrammarRule import GrammarRule
from source.grammar.GrammarRule import GrammarVariable
from source.entity.entity import Entity

def test_can_instantiate_rule():
    assert GrammarRule
    rule = GrammarRule()
    assert GrammarRule is type(rule)

def test_can_instantiate_rule_with_args():
    selections = [["a"],["b"]]
    rule = GrammarRule(selections)
    assert selections == rule.selections

def test_can_generate_rule():
    selections = [["a"],["b"]]
    rule = GrammarRule(selections)
    result = GrammarRule.generate(rule)
    assert selections[0] == result or selections[1] == result
    assert selections[0] is not result
    assert selections[1] is not result

    selections = [["a","c"],["b","d"]]
    rule = GrammarRule(selections)
    result = GrammarRule.generate(rule)
    assert selections[0] == result or selections[1] == result
    assert selections[0] is not result
    assert selections[1] is not result

def test_can_generate_recursive():
    rule_leaf = GrammarRule([["text"]])
    rule_branch = GrammarRule([[rule_leaf]])
    rule_root = GrammarRule([[rule_branch]])
    result = GrammarRule.generate(rule_root)
    assert ["text"] == result

def test_variable():
    var1 = GrammarVariable("var1")
    str1 = "var1"
    assert var1 == str1
    assert var1.__hash__() == str1.__hash__()

def test_use_variable():
    str_varname = "var_1"
    str_value = "populate"
    rule_assign = GrammarRule([[str_value]], str_varname)
    var_recall_bad = GrammarVariable("var_garbage")
    root = GrammarRule([[rule_assign, var_recall_bad]])
    try:
        result = GrammarRule.generate(root)
        assert False
    except ValueError:
        assert True

    var_recall_good = GrammarVariable(str_varname)
    root = GrammarRule([[rule_assign, var_recall_good]])
    result = GrammarRule.generate(root)
    assert str_varname == var_recall_good
    assert [str_value] == result

def test_use_variable_multi_retains_identity():
    entity = Entity()
    entity2 = Entity()
    assert entity is not entity2
    rule_assign = GrammarRule([[entity]], "var1")
    var_1 = GrammarVariable("var1")
    root = GrammarRule([[rule_assign, var_1, var_1]])
    result = GrammarRule.generate(root)
    assert entity is not result[0]
    assert entity is not result[1]
    assert result[0] is result[1]

def test_internal_var():
    # Could have assigned the vars to local variables but wanted to test that
    # creating multiple GrammarVariables works, not that there is a reason it would not.
    # Admittedly this is much less readable.
    rule_assign2 = GrammarRule([["cod"]], "var2")
    rule_assign1 = GrammarRule([[rule_assign2, GrammarVariable("var2")]], "var1")
    rule_root = GrammarRule([[rule_assign1, GrammarVariable("var1"), GrammarVariable("var2")]]) 
    result = GrammarRule.generate(rule_root)
    assert ["cod", "cod"] == result
