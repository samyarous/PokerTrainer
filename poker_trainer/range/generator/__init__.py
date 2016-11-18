from poker_trainer.range.generator.actions import *

class Generator:

    token_to_action = {
        'combination' : CombinationAction,
        'group'       : GroupAction,
        'increment'   : IncrementAction,
        'join'        : JoinAction,
        'list'        : ListAction,
        'macro'       : MacroAction,
        'percent'     : PercentAction,
        'range'       : RangeAction,
        'card'        : CardAction,
        'weight'      : WeightAction,
    }

    def get_action(self, node):
        cls = self.token_to_action.get(node.kind)
        if cls:
            return cls(self, node)
        else:
            raise KeyError("Unable to recognize token: %s" % node.kind)

    def __init__(self, root):
        self.root     = root
        self.variable = set()

    def compute_one(self, node):
        return self.get_action(node).compute()

    def compute(self):
        return self.compute_one(self.root)
