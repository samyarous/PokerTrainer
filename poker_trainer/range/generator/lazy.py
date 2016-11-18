from poker_trainer.utils.card import *
from functools import total_ordering

@total_ordering
class CardLazy:
    def __init__(self, rank=RANK_ANY, suit=SUIT_ANY):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return 'Card("%s")' % str(self)

    def __str__(self):
        return "%s%s" % (
            self.rank.upper(),
            self.suit.lower(),
        )

    def __add__(self, other):
        if isinstance(other, CardLazy):
            return HandLazy(self, other)
        else:
            return other + self

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

    def __lt__(self, other):
        rank_order = cmp_ranks(self.rank, other.rank)
        if rank_order < 0:
            return True
        if rank_order == 0 and cmp_suits(self.suit, other.suit) < 0:
            return True
        return False

@total_ordering
class HandLazy:
    def __init__(self, *cards):

        self.cards = sorted(cards)
        for _ in range(len(cards), 2):
            self.cards.append(CardLazy())

    def __repr__(self):
        return 'Hand("%s")' % str(self)

    def __str__(self):
        return ''.join([str(c) for c in self.cards])

    def __add__(self, other):
        if isinstance(other, CardLazy):
            return HandLazy(other, *self.cards)
        if isinstance(other, HandLazy):
            return HandLazy(self.cards + other.cards)
        return other + self

    def __eq__(self, other):
        return str(self) == str(other)

    def __lt__(self, other):
        l = min(len(self.hands), len(other.hands))
        for i in range(l):
            ours   = self.hands[i]
            theirs = self.hands[i]
            if ours < theirs:
                return True
        if len(self.hands) < len(other.hands):
            return True
        return False

    def expand(self):
        pass

@total_ordering
class AndSet:
    def __init__(self, *items):
        self.hands = sorted(hands)




