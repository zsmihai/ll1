import json
from Grammar.Production import Production

class ContextFreeGrammar:
    def __init__(self, non_terminals, terminals, productions, start_symbol, empty_string = "epsilon"):
        self.__non_terminals = set(non_terminals)
        self.__terminals = set(terminals)
        self.__start_symbol = start_symbol
        self.__empty_string = empty_string

        self.__productions = self.__transform_productions(productions)

        self.is_context_free_grammar()

    @staticmethod
    def __transform_productions(productions):
        productions_dict = dict()

        for lsp, production_list in productions.items():
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
                raise ValueError("Left side of production: {0} is not a terminal".format(lsp))

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

    def symbol_in_grammar(self, symbol):
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