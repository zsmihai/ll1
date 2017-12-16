from Grammar.ContextFreeGrammar import ContextFreeGrammar
from LL1.utils import concatenare_lungime_1


class FirstTable:
    def __init_first_table(self):
        self.__first_table = {}
        for terminal in self.__context_free_grammar.get_terminals():
            self.__first_table[terminal] = {terminal}
        self.__first_table[self.__context_free_grammar.get_empty_string()] = {self.__context_free_grammar.get_empty_string()}
        for nonterminal in self.__context_free_grammar.get_non_terminals():
            self.__first_table[nonterminal] = set()

        for production in self.__context_free_grammar.get_productions():
            first_of_right_side = production.get_right_side()[0]
            if self.__context_free_grammar.is_terminal(first_of_right_side):
                self.__first_table[production.get_left_side()].add(first_of_right_side)


    def __build_first_table(self):
        self.__init_first_table()

        isComplete = False

        while not isComplete:
            isComplete = True

            for production in self.__context_free_grammar.get_productions():
                first_of_rsp = self.first_for_sequence(production.get_right_side())
                if not first_of_rsp.issubset(self.__first_table[production.get_left_side()]):
                    isComplete = False
                    self.__first_table[production.get_left_side()].update(first_of_rsp)




    #input: sequence - tuple of strings
    #returns set of strings
    def first_for_sequence(self, sequence):
        if len(sequence) == 0:
            return set(self.__context_free_grammar.get_empty_string())
        if len(sequence) == 1:
            return self.__first_table[sequence[0]]

        current_set_of_symbols = self.__first_table[sequence[0]]

        for symbol in sequence[1:]:
            current_set_of_symbols = concatenare_lungime_1(self.__context_free_grammar, current_set_of_symbols, self.__first_table[symbol])

        return current_set_of_symbols


    def get_grammar(self):
        return self.__context_free_grammar

    def __init__(self, context_free_grammar : ContextFreeGrammar):
        self.__context_free_grammar = context_free_grammar
        self.__build_first_table()

