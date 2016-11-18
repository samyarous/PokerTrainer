import re
from poker_trainer.utils.format import format_tree
from poker_trainer.utils.card import *

class BaseToken:
    kind       = None
    lbp        = 0
    join_left  = False
    join_right = False

    def __init__(self, parser, position=-1, text='', values=[]):
        self.parser   = parser
        self.position = position
        self.text     = text
        self.left     = None
        self.right    = None
        self.values   = self.parse_values(values)

    def __repr__(self):
        return '%s("%s")' % (
            self.__class__.__name__,
            self.text,
        )

    def parse_values(self, values):
        return values

    def nud(self):
        raise SyntaxError(
            "%s: Syntax error (%r) at %s." %
                (self, self.text, self.position)
        )

    def led(self, left):
        raise SyntaxError(
            "%s: Unknown operator (%r) at %s." %
                (self, self.text, self.position)
        )

class EndToken(BaseToken):
    lbp = 0

class LiteralToken(BaseToken):
    kind       = 'literal'
    join_left  = True
    join_right = True

    def led(self, left):
        return self.nud()

    def nud(self):
        return self

class CardLiteral(LiteralToken):
    kind = 'card'

    def parse_values(self, values):
        self.rank = values[0] or RANK_ANY
        self.suit = values[1] or SUIT_ANY
        return values

    def __repr__(self):
        return '%s("%s%s")' % (
                self.__class__.__name__,
                self.rank.upper(),
                self.suit.lower(),
            )

class SuitLiteral(LiteralToken):
    kind = 'suit'

class JoinOperator(BaseToken):
    kind = 'join'
    lbp  = 100

    def led(self, left):
        right = self.parser.expression(self.lbp)
        self.left  = left
        self.right = right
        return self

class PercentToken(LiteralToken):
    kind = 'percent'
    accepted = ('3H','6H','10H','ES','VR')

    def nud(self):
        return self

    def parse_values(self, values):
        result = {}
        if len(filter(lambda x: x, values)) % 2 == 0:
            # pair, this means we have a ranking
            result['ranking'] = values[-1].upper()
        else:
            result['ranking'] = '10H'
        if values[1] == '-':
            # we have a range
            result['from'] = int(values[0])
            result['to']   = int(values[2])
        else:
            result['from'] = 0
            result['to']   = int(values[0])
        if result['ranking'] not in self.accepted:
            raise ValueError(
                'Percent Ranking not found: %s at %s. Legal values are %s' % (
                    result['ranking'],
                    self.text,
                    self.accepted
                )
            )
        return result

    def __repr__(self):
        return '%s("%s%%-%s%%[%s]")' % (
            self.__class__.__name__,
            self.values['from'],
            self.values['to'],
            self.values['ranking'],
        )

class ListStart(LiteralToken):
    kind = 'list'
    join_left  = True
    join_right = False

    def nud(self):
        try:
            expr = self.parser.expression()
            current = self.parser.next()
        except StopIteration:
            raise SyntaxError("Unexpected end of string.")
        if current.kind != 'list_close':
            raise SyntaxError(') expected at %s found %s instead.' %
                (
                    current.position,
                    current.text,
                )
            )
        self.right = expr
        return self



    def __repr__(self):
        return '%s("()")' % self.__class__.__name__

class ListEnd(LiteralToken):
    kind = 'list_close'
    join_left  = False
    join_right = True

class GroupStart(LiteralToken):
    kind = 'group'
    join_left  = True
    join_right = False

    def nud(self):
        try:
            expr = self.parser.expression()
            current = self.parser.next()
        except StopIteration:
            raise SyntaxError("Unexpected end of string.")
        if current.kind != 'group_close':
            raise SyntaxError('] expected at %s found %s instead.' %
                (
                    current.position,
                    current.text,
                )
            )
        self.right = expr
        return self

    def __repr__(self):
        return '%s("[]")' % self.__class__.__name__

class GroupEnd(LiteralToken):
    kind = 'group_close'
    join_left  = False
    join_right = True

class WeightOperator(BaseToken):
    kind = 'weight'
    lbp  = 20

    def parse_values(self, values):
        return {'weight': values[0]}

    def led(self, left):
        self.left = left
        return self

    def __repr__(self):
        return '%s("@%s")' % (
            self.__class__.__name__,
            self.values['weight'],
        )

class IncrementOperator(BaseToken):
    kind = 'increment'
    lbp  = 60

    def led(self, left):
        self.left = left
        return self

class RangeOperator(BaseToken):
    kind = 'range'
    lbp  = 60

    def led(self, left):
        self.left  = left
        next_token = self.parser.current()
        if next_token.kind == 'card':
            self.right = self.parser.expression(self.lbp)
        return self

class CombinationOperator(BaseToken):
    kind = 'combination'

    op_to_text = {
        ',': 'or',
        '!': 'xor',
        ':': 'and',
    }

    @property
    def lbp(self):
        if self.text in '!:':
            return 40
        else:
            return 10

    def led(self, left):
        try:
            right = self.parser.expression(self.lbp)
        except StopIteration:
            raise SyntaxError("Unexpected end of string.")
        self.left  = left
        self.right = right
        return self

class MacroOperator(BaseToken):
    kind = 'macro'
    lbp  = 20

    def parse_values(self, values):
        if values[0].lower() not in 'bflmnorswz':
            raise ValueError(
                'Macro "%s" is not supported at %s' %
                    (values[0], self.position + 1)
            )

    def led(self, left):
        self.left = left
        return self
