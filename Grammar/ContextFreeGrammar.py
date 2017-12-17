import json
from Grammar.Production import Production


class ContextFreeGrammar:
    def __init__(self, non_terminals, terminals, productions, start_symbol, empty_string="epsilon",
                 substitution_map=None):
        self.__non_terminals = set(non_terminals)
        self.__terminals = set(terminals)
        self.__start_symbol = start_symbol
        self.__empty_string = empty_string

        self.__substitution_map = substitution_map
        self.__productions = productions

        self.__perform_substitution()
        self.__productions = self.__transform_productions()

        self.is_context_free_grammar()

    def __transform_productions(self):
        productions_dict = dict()

        for lsp, production_list in self.__productions.items():
            productions_for_lsp = []
            for production in production_list:
                productions_for_lsp.append(Production(lsp, production))
            productions_dict[lsp] = productions_for_lsp

        return productions_dict

    @staticmethod
    def read_grammar_from_file(filename):
        with open(filename) as file:
            data = json.load(file)
        return ContextFreeGrammar(**data)

    def get_terminals(self):
        return self.__terminals

    def get_non_terminals(self):
        return self.__non_terminals

    def get_start_symbol(self):
        return self.__start_symbol

    def get_empty_string(self):
        return self.__empty_string

    def get_productions_for_non_terminal(self, non_terminal):
        return self.__productions.get(non_terminal, [])

    def __are_lsps_non_terminal(self):
        for lsp in self.__productions:
            if lsp not in self.__non_terminals:
                raise ValueError("Left side of production: {0} is not a non_terminal".format(lsp))

    def __check_terminals_nonterminals(self):
        intersection = self.__terminals.intersection(self.__non_terminals)
        if len(intersection) != 0:
            raise ValueError("Elements: {0} cannot be both terminals and nonterminals".format(intersection))
        if self.__empty_string in self.__non_terminals:
            raise ValueError("Empty string cannot be in nonterminals")
        if self.__empty_string in self.__terminals:
            raise ValueError("Empty string cannot be in terminals")

    def is_context_free_grammar(self):
        self.__check_terminals_nonterminals()
        self.__are_lsps_non_terminal()
        self.__check_productions()

    def is_symbol_in_grammar(self, symbol):
        return symbol in self.__non_terminals or symbol in self.__terminals or symbol == self.__empty_string

    def is_terminal(self, symbol):
        return symbol in self.__terminals

    def is_nonterminal(self, symbol):
        return symbol in self.__non_terminals

    def is_empty_string(self, symbol):
        return symbol == self.__empty_string

    def get_productions(self):
        productions = []
        for lsp, rsp in self.__productions.items():
            productions.extend(rsp)
        return productions

    @staticmethod
    def get_test_grammar():
        return ContextFreeGrammar.read_grammar_from_file("testGrammar.json")

    def __check_productions(self):
        for production in self.get_productions():
            if not self.is_symbol_in_grammar(production.get_left_side()):
                raise ValueError("{0} not a valid symbol in grammar".format(production.get_left_side))
            for symbol in production.get_right_side():
                if not self.is_symbol_in_grammar(symbol):
                    raise ValueError("{0} not a valid symbol in grammar".format(symbol))

    def __perform_substitution(self):
        if self.__substitution_map is None:
            return

        to_be_substituted = self.__substitution_map.keys()
        self.__non_terminals = {self.__substitution_map.get(non_terminal, non_terminal) for non_terminal in
                                self.__non_terminals}

        self.__terminals = {self.__substitution_map.get(terminal, terminal) for terminal in
                                self.__terminals}

        self.__start_symbol = self.__substitution_map.get(self.__start_symbol, self.__start_symbol)
        self.__empty_string = self.__substitution_map.get(self.__empty_string, self.__empty_string)

        new_productions = {}

        for left_side, right_lists in self.__productions.items():
            left_side = self.__substitution_map.get(left_side, left_side)

            right_lists = [[self.__substitution_map.get(symbol, symbol) for symbol in right_side] for right_side in
                           right_lists]
            new_productions[left_side] = right_lists

        self.__productions = new_productions
