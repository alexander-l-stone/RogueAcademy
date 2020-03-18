import pytest
from source.grammar.GrammarRule import GrammarRule

def test_can_instantiate_rule():
    assert GrammarRule
    test_rule = GrammarRule()
    assert isinstance(test_rule, GrammarRule)

def test_can_instantiate_rule_with_args():
    test_selections = [["a"],["b"]]
    test_rule = GrammarRule(test_selections)
    assert isinstance(test_rule, GrammarRule)
    assert test_rule.selections == test_selections

def test_can_generate_rule():
    test_selections = [["a"],["b"]]
    test_rule = GrammarRule(test_selections)
    result = GrammarRule.generate(test_rule)
    assert result == test_selections[0] or result == test_selections[1]
    assert result is not test_selections[0]
    assert result is not test_selections[1]

    test_selections = [["a","c"],["b","d"]]
    test_rule = GrammarRule(test_selections)
    result = GrammarRule.generate(test_rule)
    assert result == test_selections[0] or result == test_selections[1]
    assert result is not test_selections[0]
    assert result is not test_selections[1]
