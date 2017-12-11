
#firstSet, secondSet: seturi de stringuri
def concatenare_lungime_1(contextFreeGrammar, firstSet:set, secondSet):

    if len(firstSet) == 0 or len(secondSet) == 0:
        return set()

    concatenare = set()
    for sequence in firstSet:
        if not contextFreeGrammar.is_empty_string(sequence):
            concatenare.add(sequence)

    if contextFreeGrammar.get_empty_string() in firstSet:
        for sequence in secondSet:
            concatenare.add(sequence)

    return concatenare