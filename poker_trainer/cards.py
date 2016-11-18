import eval7
import random

from functools import total_ordering

@total_ordering
class Card(eval7.Card):
    def __init__(self, name):
        super(self.__class__, self).__init__(name)
        self.name = name

    def __repr__(self):
        return 'Card("%s")' % self.name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if isinstance(other, str):
            return other == self.name
        else:
            return self.suit == other.suit and self.rank == other.rank

    def __lt__(self, other):
        if isinstance(other, str):
            other = Card(other)
        if self.rank != other.rank:
            return self.rank < other.rank
        else:
            return self.suit < other.suit

    def __add__(self, other):
        return Hand(self, other)

@total_ordering
class Hand:
    def __init__(self, *items):
        cards = []
        for item in items:
            if isinstance(item, str):
                cards += [Card(item[x:x+2]) for x in range(0, len(item), 2)]
            elif hasattr(item, 'cards'):
                cards += item.cards
            else:
                cards += [item]

        self.cards = list(reversed(sorted(set(cards))))
        self.name  = ''.join([c.name for c in self.cards])
        self.mask  = eval7.evaluate(self.cards)
        super().__init__()

    def __eq__(self, other):
        if isinstance(other, str):
            return other == self.name
        else:
            return self.mask == other.mask

    def __lt__(self, other):
        if isinstance(other, str):
            other = Card(other)
        if self.mask != other.mask:
            return self.mask < other.mask
        elif len(self.cards) != len(other.cards):
            return self.cards < other.cards
        else:
            for i in range(len(self.cards)):
                this_card  = self.cards[i]
                other_card = other.cards[i]
                if this_card != other_card:
                    return this_card < other_card
        return False


    def __add__(self, other):
        return Hand(self.hands + other.hands)

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return 'Hand("%s")' % (self.name)


class Deck(object):
    def __init__(self):
        self.cards = set()
        self.order = list()

        for card in ALL_CARDS:
            self.cards.add(card)
            self.order.append(card)

    def shuffle(self):
        random.shuffle(self.order)
        return self

    def sample(self, n):
        return random.sample(list(self.peek), n)

    def deal(self, number):
        return [self.pop() for _ in range(number)]

    def peek(self):
        for card in self.order:
            if card in self.cards:
                yield card

    def pop(self):
        for card in self.peek():
            self.remove(card)
            return card

    def remove(self, card):
        if isinstance(card, str):
            card = Card(card)
        if card in self.cards:
            self.cards.remove(card)
        return self

    def add(self, card):
        if isinstance(card, str):
            card = Card(card)
        self.cards.add(card)
        return self

    def __len__(self):
        return len(self.cards)

    def __repr__(self):
        return 'Deck("%s")' % ','.join(
            [c.name for c in self.peek()]
        )


SUITS = eval7.cards.suits
RANKS = eval7.cards.ranks
ALL_CARDS = [
    Card("%s%s" % (rank, suit)) for rank in RANKS for suit in SUITS
]
