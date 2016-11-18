from poker_trainer.utils.format import format_tree
from poker_trainer.range.parser import Parser
from poker_trainer.range.generator import Generator

if __name__ == '__main__':
    import sys
    for t in sys.argv[1:]:
        p = Parser(t)
        root = p.parse()
        print(format_tree(root))
        print(repr(Generator(root).compute()))
