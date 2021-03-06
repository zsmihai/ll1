from Grammar.ContextFreeGrammar import ContextFreeGrammar
from LL1.FollowTable import FollowTable
from LL1.firstTable import FirstTable


class ParseTable:

    def is_accept(self, symbol):
        return symbol == "acc"

    def is_pop(self, symbol):
        return symbol == "pop"

    def get_empty_stack(self):
        return self.__empty_stack

    def is_production_index(self, symbol):
        return symbol in self.__indexed_productions.keys()

    def get_grammar(self):
        return self.__grammar

    def get_production_for_index(self, index):
        return self.__indexed_productions.get(index, None)

    def __getitem__(self, key):
        return self.__table.get(key, None)

    def __create_empty_stack_symbol(self):
        empty_stack = "$"
        while self.__grammar.is_symbol_in_grammar(empty_stack):
            empty_stack += "$"
        self.__empty_stack = empty_stack

    def __create_production_indexing(self):
        indexed_productions = {}

        for production_index, production in enumerate(self.__grammar.get_productions()):
            indexed_productions[production_index] = production

        self.__indexed_productions = indexed_productions

    def __init__(self, context_free_grammar: ContextFreeGrammar, first_table: FirstTable, follow_table: FollowTable):
        self.__grammar = context_free_grammar
        self.__first_table = first_table
        self.__follow_table = follow_table

        self.__create_production_indexing()
        self.__create_empty_stack_symbol()

        self.__create_parse_table()

    def __init_parse_table(self):
        self.__table = {}
        for terminal in self.__grammar.get_terminals():
            self.__table[(terminal, terminal)] = "pop"
        self.__table[(self.__empty_stack, self.__empty_stack)] = "acc"

    def __add_to_table(self, key, value):
        if self.__table.get(key, None) is not None:
            raise Exception(
                "Conflict in parse table! Found M({0}) = {1} while trying to add {2}".format(key, self.__table[key],
                                                                                             value))
        self.__table[key] = value

    def __create_parse_table(self):
        self.__init_parse_table()

        for production_index, production in self.__indexed_productions.items():

            first_of_right_side = self.__first_table.first_for_sequence(production.get_right_side())

            for terminal in first_of_right_side:
                if not self.__grammar.is_empty_string(terminal):
                    key = (production.get_left_side(), terminal)
                    self.__add_to_table(key, production_index)
                else:
                    follow_of_left_side = self.__follow_table.get_table()[production.get_left_side()]
                    for follow_non_terminal in follow_of_left_side:
                        key = (production.get_left_side(), follow_non_terminal if not self.__grammar.is_empty_string(
                            follow_non_terminal) else self.__empty_stack)
                        self.__add_to_table(key, production_index)
