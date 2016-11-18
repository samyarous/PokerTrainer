#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module contains helper function that format things
"""

from colored import fg, attr, bg
import itertools

suit_colors = {
    0: 'light_green',
    1: 'light_blue',
    2: 'light_red',
    3: 'grey_70',
}

def colored(str, color):
    return "%s%s%s" % (fg(color), str, attr('reset'))

def format_card(card):
    color = suit_colors[card.suit]
    return colored(card.name, color)


def format_cards(obj):
    if hasattr(obj, 'cards'):
        cards = obj.cards
    else:
        cards = [obj]
    return ''.join(
        [format_card(c) for c in cards]
    )




FORK = u'\u251c'
LAST = u'\u2514'
VERTICAL = u'\u2502'
HORIZONTAL = u'\u2500'


def _format_tree(node, color, prefix=''):
    children = [x for x in (node.left, node.right) if x]
    next_color = (color + 1) % 2
    next_prefix = u''.join([prefix, VERTICAL, u'   '])
    for child in children[:-1]:
        yield u''.join([
            prefix,
            FORK,
            HORIZONTAL,
            HORIZONTAL,
            u' ',
            colored(str(child),suit_colors[next_color])
        ])
        if child:
            for result in _format_tree(child, next_color, next_prefix):
                yield result
    if children:
        last_prefix = u''.join([prefix, u'    '])
        yield u''.join([
            prefix,
            LAST,
            HORIZONTAL,
            HORIZONTAL,
            u' ',
            colored(str(children[-1]), suit_colors[next_color])
        ])
        if children[-1]:
            for result in _format_tree(children[-1], next_color, last_prefix):
                yield result


def format_tree(node):
    lines = itertools.chain(
        ['-' * 30],
        [u''],
        [colored(str(node), suit_colors[0])],
        _format_tree(node, 0),
        [u''],
        ['-' * 30],
    )
    return u'\n'.join(lines)





