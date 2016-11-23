from collections import OrderedDict
import re

from poker_trainer.range.parser.tokens import *

class Parser:
    ranks    = 'ABEFGIJKLMNOPQRTUV23456789*'
    suits    = 'SHDCWXYZ'
    language = OrderedDict([
        (
            re.compile('(\d+)%(?:(-)(\d+)%)?(\w+)?', re.IGNORECASE),
            PercentToken,
        ),
        (
            re.compile('@(\d+)', re.IGNORECASE),
            WeightOperator,
        ),
        (
            re.compile('\(', re.IGNORECASE),
            ListStart,
        ),
        (
            re.compile('\)', re.IGNORECASE),
            ListEnd,
        ),
        (
            re.compile('\[', re.IGNORECASE),
            GroupStart,
        ),
        (
            re.compile('\]', re.IGNORECASE),
            GroupEnd,
        ),
        (
            re.compile('\+', re.IGNORECASE),
            IncrementOperator,
        ),
        (
            re.compile('\-', re.IGNORECASE),
            RangeOperator,
        ),
        (
            re.compile(
                '(%s)?(%s)?' % (
                    '[ABEFGIJKLMNOPQRTUV23456789]',
                    '[SHDCWXYZ]',
                ),
                re.IGNORECASE
            ),
            CardLiteral,
        ),
        (
            re.compile('\$([A-Z])', re.IGNORECASE),
            MacroOperator,
        ),
        (
            re.compile('[\,\:\!]', re.IGNORECASE),
            CombinationOperator,
        ),
    ])


    def __init__(self, range_str):
        self.range_str = range_str
        self.index     = 0

    def parse(self):
        self.tokenize()
        print(self.tokens)
        return self.expression()

    def expression(self, rbp=0):
        t     = self.current()
        self.next()
        left  = t.nud()
        while rbp < self.current().lbp:
            t = self.current()
            self.next()
            left = t.led(left)
        return left


    def tokenize(self):
        remaining_start = 0
        left = None
        self.tokens     = []
        while(remaining_start < len(self.range_str)):
            matched = False
            for reg, token_class in self.language.items():
                m = reg.match(self.range_str, remaining_start)

                if m and m.group(0): # do not match empty string
                    print (reg.pattern, self.range_str, m.group(0))
                    remaining_start = m.end()
                    instance = token_class(
                        self,
                        m.start(),
                        m.group(0),
                        m.groups()
                    )
                    if left and left.join_right and instance.join_left:
                        # we have two literal next to each other
                        # add a join operator
                        self.tokens.append(JoinOperator(self,))
                    left = instance
                    self.tokens.append(instance)
                    matched = True
                    break
            if not matched:
                raise SyntaxError(
                    "at %s: %s" % (
                        remaining_start + 1,
                        self.range_str[remaining_start:],
                    )
                )
        self.tokens += [EndToken(self, len(self.range_str))]
        return self.tokens

    def reset(self):
        self.index = 0

    def current(self):
        if self.index >= len(self.tokens):
            raise StopIteration()
        return self.tokens[self.index]

    def peek(self):
        if (self.index + 1) >= len(self.tokens):
            raise StopIteration()
        return self.tokens[self.index + 1]

    def next(self):
        self.index += 1
        if self.index >= len(self.tokens):
            raise StopIteration()
        return self.tokens[self.index - 1]

    def __iter__(self):
        return self.tokens.__iter__()
