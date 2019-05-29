import tree
import graphviz
import sys
from data import Data
from fractions import Fraction


class ProbNode(tree.Node):
    def get_pw(self, beta):
        if self.is_leaf():
            return self.pe
        else:
            sub = (1 - beta) * \
                tree.product(c.pw for c in self.children if c is not None)
            return beta * self.pe + sub

    def get_pm(self, beta):
        if self.is_leaf():
            return self.pe
        else:
            left = beta * self.pe
            right = (1 - beta) * \
                tree.product(c.pm for c in self.children if c is not None)
            if left > right:
                self.should_prune = True
            return max(left, right)

    def compute_probas(self, beta):
        for c in self.children:
            if c is not None:
                c.compute_probas(beta)
        self.pe = self.get_pe()
        self.pw = self.get_pw(beta)
        self.should_prune = False
        self.pm = self.get_pm(beta)

    def prune(self):
        if self.should_prune:
            self.children = [None] * self.m
        else:
            for c in self.children:
                if c is not None:
                    c.prune()

    def graphviz(self):
        return [
            ("pe", "pe", graphviz.str_fraction),
            ("pw", "pw", graphviz.str_fraction),
            ("pm", "pm", graphviz.str_fraction),
            ("as", "count", None)
        ]


def prune_tree_main(data, m, D, beta):
    top = ProbNode(None, m)
    print("Building tree", file=sys.stderr)
    tree.build_counts(top, data, D, lambda value, m: ProbNode(value, m))
    print("Computing probas", file=sys.stderr)
    top.compute_probas(beta)
    top.prune()
    print(graphviz.main_node_to_graphviz(top))
    return top


if __name__ == "__main__":
    path = "../dataprojet2.txt"
    data = Data(path)

    prune_tree_main(data.data, m=data.m, D=9, beta=Fraction(1, 2))
