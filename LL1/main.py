from Grammar.ContextFreeGrammar import ContextFreeGrammar
from LL1.FollowTable import FollowTable
from LL1.ParseTable import ParseTable
from LL1.Parser import Parser
from LL1.firstTable import FirstTable

def read_sequence(sequence_file):
    with open(sequence_file) as file:
        sequence = file.read()

    return sequence.split()[::2]

if __name__ == "__main__":
    grammar_file = "testGrammar.json"
    sequence_file = "first.in.pif"

    grammar = ContextFreeGrammar.read_grammar_from_file(grammar_file)
    first_table = FirstTable(grammar)
    follow_table = FollowTable(first_table)
    parse_table = ParseTable(grammar, first_table, follow_table)

    sequence = read_sequence(sequence_file)

    parsed_string = Parser(parse_table, sequence)

    print(parsed_string.get_as_derivations_string_as_string())