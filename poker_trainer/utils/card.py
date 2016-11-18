RANK_ANY      = '*'
SUIT_ANY      = '#'

# order of suits in reverse
# as we show cards from the left
SUITS = {
    's': 1,
    'h': 2,
    'd': 3,
    'c': 4,
}

# order of ranks in reverse
# as we show cards from the left
RANKS = {
    'A': 1,
    'K': 2,
    'Q': 3,
    'J': 4,
    'T': 5,
    '9': 6,
    '8': 7,
    '7': 8,
    '6': 9,
    '5': 10,
    '4': 11,
    '3': 12,
    '2': 13,
}

ALL_SUITS     = ''.join(SUITS.keys())
ALL_RANKS     = ''.join(RANKS.keys())


def cmp_ranks(r1, r2):
    r1_key = str(RANKS.get(r1.upper(), r1.upper()))
    r2_key = str(RANKS.get(r2.upper(), r2.upper()))
    return (r1_key > r2_key) - (r1_key < r2_key)

def cmp_suits(s1, s2):
    s1_key = RANKS.get(s1.upper(), s1.upper())
    s2_key = RANKS.get(s2.upper(), s2.upper())
    return (s1_key > s2_key) - (s1_key < s2_key)

