from __future__ import absolute_import, print_function

from .corpus import common_cmudict


def find_minimal_pairs(target1, target2, position):
    subset1 = {}
    subset2 = {}
    for word, pronunciations in common_cmudict.items():
        if position == "initial":
            index = 0
        elif position == "final":
            index = -1

        for pronunciation in pronunciations:
            if pronunciation[index] == target1:
                subset1[word] = pronunciation
            elif pronunciation[index] == target2:
                subset2[word] = pronunciation

    results = []
    for word1, pron1 in subset1.items():
        for word2, pron2 in subset2.items():
            if len(pron1) == len(pron2):
                if (position == "initial" and pron2 == [target2, ] + pron1[1:]) or \
                        (position == "final" and pron2 == pron1[:-1] + [target2, ]):
                    results.append((word1, word2))
    return results
