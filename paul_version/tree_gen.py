import tree
import random

class TreeGenerator:
    def __init__(self, tree):
        self.tree = tree
        self.past = []

    def next(self):
        node = self.tree
        for c in reversed(self.past):
            next_node = node.children[c]
            if next_node:
                node = next_node
            else:
                break
        next_value = random.choices(range(node.m), node.count)[0]
        self.past.append(next_value)
        return next_value