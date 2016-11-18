from poker_trainer.range.generator.lazy import *

class BaseAction:
    def __init__(self, generator, node):
        self.node = node
        self.generator = generator

    def compute_children(self):
        if self.node and self.node.left:
            self.left_result = self.generator.compute_one(self.node.left)
        if self.node and self.node.right:
            self.right_result = self.generator.compute_one(self.node.right)

    def compute(self):
        raise NotImplementedError()

class JoinAction(BaseAction):
    def compute(self):
        self.compute_children()
        return self.left_result + self.right_result

class CardAction(BaseAction):
    def compute(self):
        rank = self.node.rank
        suit = self.node.suit
        return CardLazy(rank, suit)


class PercentAction(BaseAction):
    def compute(self):
        raise NotImplementedError()

class ListAction(BaseAction):
    def compute(self):
        return self.right_result

class GroupAction(BaseAction):
    def compute(self):
        raise NotImplementedError()

class WeightAction(BaseAction):
    def compute(self):
        raise NotImplementedError()

class IncrementAction(BaseAction):
    def compute(self):
        raise NotImplementedError()

class RangeAction(BaseAction):
    def compute(self):
        raise NotImplementedError()

class CombinationAction(BaseAction):
    def compute(self):
        raise NotImplementedError()

class MacroAction(BaseAction):
    def compute(self):
        raise NotImplementedError()
