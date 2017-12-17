from Grammar.ContextFreeGrammar import ContextFreeGrammar
from LL1.FollowTable import FollowTable
from LL1.ParseTable import ParseTable
from LL1.firstTable import FirstTable


class Parser:

    def __get_next_of_sequence(self):
        try:
            next_elem = next(self.__sequence_iterator)
        except StopIteration:
            next_elem = self.__parse_table.get_empty_stack()
        return next_elem

    def __init__(self, parse_table : ParseTable, sequence):
        self.__parse_table = parse_table

        self.__production_list = []
        self.__work_stack = [parse_table.get_empty_stack(), parse_table.get_grammar().get_start_symbol()]
        self.__sequence_iterator = iter(sequence)
        current_symbol = self.__get_next_of_sequence()

        while True:

            parse_table_symbol = parse_table[(self.__work_stack[-1], current_symbol)]

            if self.__parse_table.is_accept(parse_table_symbol):
                break

            if self.__parse_table.is_pop(parse_table_symbol):
                current_symbol = self.__get_next_of_sequence()
                self.__work_stack.pop()

            elif self.__parse_table.is_production_index(parse_table_symbol):
                production = self.__parse_table.get_production_for_index(parse_table_symbol)

                self.__production_list.append(parse_table_symbol)
                self.__work_stack.pop()
                self.__work_stack.extend((symbol for symbol in  production.get_right_side()[::-1] if not grammar.is_empty_string(symbol)))

            else:
                raise Exception("Error for {0}".format((self.__work_stack[-1], current_symbol)))


if __name__ == "__main__":
    grammar = ContextFreeGrammar.get_test_grammar()
    ff = FirstTable(grammar)
    flt = FollowTable(ff)
    pt = ParseTable(grammar, ff, flt)
    parsed = Parser(pt, [3,                 0, 13,              0,  21,           1,    4,    3 ])
    print("a")