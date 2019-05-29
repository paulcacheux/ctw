from fractions import Fraction
import graphviz


class Node:
    def __init__(self, value, m):
        self.m = m
        self.value = value
        self.children = [None] * m
        self.count = [0] * m
        self.pe = None

    def is_leaf(self):
        return all(c is None for c in self.children)

    def get_pe(self):
        Ms = sum(self.count)
        if Ms == 0:
            return Fraction(1, 1)

        num = 1
        for j in range(self.m):
            for i in range(self.count[j]):
                num *= Fraction(1, 2) + i

        den = 1
        for i in range(Ms):
            den *= Fraction(self.m, 2) + i

        res = num / den
        return res

    def compute_probas(self, beta):
        for c in self.children:
            if c is not None:
                c.compute_probas(beta)
        self.pe = self.get_pe()

    def graphviz(self):
        return [
            ("pe", "pe", graphviz.str_fraction),
            ("as", "count", None)
        ]


def build_counts(top_node, data, D, node_builder):
    m = top_node.m
    for width in range(1, D+1):
        for start in range(len(data) - width + 1):
            context = data[start:start+width]
            value = context[-1]
            pre = context[:-1]
            insert_node = top_node
            for c in reversed(pre):
                # shouldn't append in kTree so we can build a Node and not a KTreeNode
                if insert_node.children[c] is None:
                    insert_node.children[c] = node_builder(c, m)
                insert_node = insert_node.children[c]
            insert_node.count[value] += 1


def product(iter):
    res = Fraction(1, 1)
    for elem in iter:
        res *= elem
    return res
