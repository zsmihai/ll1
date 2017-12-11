from Grammar.ContextFreeGrammar import ContextFreeGrammar


class FollowTable:
    def __init__(self,
                 context_free_grammar: ContextFreeGrammar,
                 first_table: FirstTable):
        self.__table = {}
        f = {}
        non_terminals = context_free_grammar.get_non_terminals()
        for non_terminal in non_terminals:
            if non_terminal is not context_free_grammar.get_start_symbol():
                f[non_terminal] = set()
            else:
                f[non_terminal] = {context_free_grammar.get_empty_string()}
        modified = False
        while not modified:
            for production in context_free_grammar.get_productions():
                right = production.get_right_side()
                for index in range(len(right)):
                    symbol = right[index]
                    if context_free_grammar.is_nonterminal(symbol):
                        sub_sequence = right[index + 1:]
                        if context_free_grammar.get_empty_string() in sub_sequence:
                            self.__table[symbol].union(self.__table[production.get_left_side()])
                        if len(sub_sequence) > 0:
                            self.__table[symbol].union(first_table.first_for_sequence(sub_sequence))

    def get_table(self):
        return self.__table
