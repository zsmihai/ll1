import json

from Grammar.ContextFreeGrammar import ContextFreeGrammar
from LL1.FollowTable import FollowTable
from LL1.firstTable import FirstTable
import os

def compare_first_table(context_free_grammar, first_table, expected_first_table):

    for non_terminal in context_free_grammar.get_non_terminals():
        set_from_table = first_table.first_for_sequence((non_terminal,))
        expected_set = set(expected_first_table[non_terminal])
        if set_from_table != expected_set:
            raise Exception("First table wrong for terminal {0}. Expected {1}, got {2}".format(non_terminal,expected_set, set_from_table))


def compare_follow_table(context_free_grammar, follow_table, expected_follow_table):
    follow_table_values = follow_table.get_table()
    for non_terminal in context_free_grammar.get_non_terminals():
        expected_set = set(expected_follow_table[non_terminal])
        if follow_table_values[non_terminal] != expected_set:
            raise Exception(
                "Follow table wrong for terminal {0}. Expected {1}, got {2}".format(non_terminal, expected_set,
                                                                                    follow_table_values[non_terminal]))



def testgrammar(test_data):

    context_free_grammar = ContextFreeGrammar(**test_data["grammar"])
    first_table = FirstTable(context_free_grammar)
    follow_table = FollowTable(first_table)

    compare_first_table(context_free_grammar, first_table, test_data["first_table"])
    compare_follow_table(context_free_grammar, follow_table, test_data["follow_table"])


if __name__ == "__main__":

    test_dir = "tests"

    for root, dirs, filenames in os.walk(test_dir):
        for f in filenames:
            print("Running testfile {0}".format(f))
            with open(os.path.join(test_dir, f) ) as file:
                test_data = json.load(file)
            testgrammar(test_data)