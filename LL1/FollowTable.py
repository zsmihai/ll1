from Grammar.ContextFreeGrammar import ContextFreeGrammar
from LL1.firstTable import FirstTable


class FollowTable:
    def __init__(self,
                 context_free_grammar: ContextFreeGrammar,
                 first_table: FirstTable):
        self.__table = {}
        non_terminals = context_free_grammar.get_non_terminals()
        for non_terminal in non_terminals:
            if non_terminal != context_free_grammar.get_start_symbol():
                self.__table[non_terminal] = set()
            else:
                self.__table[non_terminal] = {context_free_grammar.get_empty_string()}
        modified = True
        while modified:
            modified = False
            for production in context_free_grammar.get_productions():
                right = production.get_right_side()
                for index in range(len(right)):
                    symbol = right[index]
                    if context_free_grammar.is_nonterminal(symbol):
                        sub_sequence = right[index + 1:]
                        set_for_update = set()
                        if context_free_grammar.get_empty_string() in sub_sequence or len(sub_sequence) == 0:
                            set_for_update.update(self.__table[production.get_left_side()])
                        if len(sub_sequence) > 0:
                            set_for_update.update(first_table.first_for_sequence(sub_sequence))
                        if not set_for_update.issubset(self.__table[symbol]) :
                            modified = True
                            self.__table[symbol].update(set_for_update)

    def get_table(self):
        return self.__table

g = ContextFreeGrammar.get_test_grammar()
ft = FirstTable(g)
ff = FollowTable(g, ft)
print("pi")