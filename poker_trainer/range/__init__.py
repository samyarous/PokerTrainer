import os
import math

from poker_trainer.cards import SUITS, RANKS, Hand

def load_hand_order():
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    files = {
        '3H'  : 'static/he3maxordering.txt',
        '6H'  : 'static/he6maxordering.txt',
        'ES'  : 'static/heequitysquaredordering.txt',
        '10H' : 'static/heordering.txt',
        'VR'  : 'static/hevsrandomordering.txt',
    }

    by_percent = {
        '3H' : {i: set() for i in range(0, 100 + 1)},
        '6H' : {i: set() for i in range(0, 100 + 1)},
        'ES' : {i: set() for i in range(0, 100 + 1)},
        '10H': {i: set() for i in range(0, 100 + 1)},
        'VR' : {i: set() for i in range(0, 100 + 1)},
    }

    for key, path in files.items():
        work_set = set()
        with open(os.path.join(__location__, path)) as f:
            for line in f:
                combinations = expand_range(line.strip())
                previous     = math.ceil(len(work_set) * 100 / 1326)
                work_set.update(combinations)
                current      = math.ceil(len(work_set) * 100 / 1326)
                if current != previous:
                    # we have a new step
                    by_percent[key][current].update(
                        by_percent[key][previous]
                    )
                by_percent[key][current].update(combinations)
    return by_percent


def expand_ranges(range):
    # first we need to split the ranges
    pass

def expand_range(range):
    hands = set()
    suits_in_order = list(reversed(SUITS))
    if len(range) == 4:
        # we have a suited combination
        for suit in suits_in_order:
            hands.add(Hand(''.join((range[0], suit, range[2], suit,))))
    else:
        for suit1 in suits_in_order:
            for suit2 in suits_in_order:
                if suit1 != suit2:
                    hands.add(Hand(''.join((range[0], suit1, range[1], suit2,))))
    return list(reversed(sorted(hands)))

