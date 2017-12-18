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

    def __init__(self, parse_table: ParseTable, sequence):
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
                self.__work_stack.extend(
                    (symbol for symbol in production.get_right_side()[::-1] if not parse_table.get_grammar().is_empty_string(symbol)))

            else:
                raise Exception("Error for {0}".format((self.__work_stack[-1], current_symbol)))

    def get_as_derivations_string(self):
        derivations_string = [[self.__parse_table.get_grammar().get_start_symbol()]]
        for production_index in self.__production_list:
            production = self.__parse_table.get_production_for_index(production_index)

            left_symbol = production.get_left_side()
            if left_symbol not in derivations_string[-1]:
                raise ValueError("Error during derivation_string generation! Symbol {0} not found".format(left_symbol))

            index = derivations_string[-1].index(left_symbol)

            new_derivation_string = derivations_string[-1][:index]
            new_derivation_string.extend(symbol for symbol in production.get_right_side() if
                                         not self.__parse_table.get_grammar().is_empty_string(symbol))
            new_derivation_string.extend(derivations_string[-1][index + 1:])
            derivations_string.append(new_derivation_string)

        return derivations_string

    def get_as_derivations_string_as_string(self):
        derivations_string = self.get_as_derivations_string()

        return "->\n".join(" ".join([str(derivation_symbol) for derivation_symbol in derivation_elem]) for derivation_elem in derivations_string)


if __name__ == "__main__":
    grammar = ContextFreeGrammar.get_test_grammar()
    ff = FirstTable(grammar)
    flt = FollowTable(ff)
    pt = ParseTable(grammar, ff, flt)
    parsed = Parser(pt, [3, 0, 13, 0, 21, 1, 4, 3])
    print(parsed.get_as_derivations_string_as_string())
