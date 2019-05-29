# -*- coding: utf-8 -*-

from fractions import Fraction
import markov
import graphviz
import numpy as np
import sys
import tree
from data import Data


def ij_iterator(kj, m):
    r = range(1, kj + 1)
    if m == 1:
        for i in r:
            yield (i,)
    else:
        for left in ij_iterator(kj, m - 1):
            for i in r:
                yield (*left, i)


class KTreeNode(tree.Node):
    def __init__(self, value, m, k):
        super(KTreeNode, self).__init__(value, m)
        self.k = k
        self.pms = [0] * k
        self.Bs = np.zeros((k, m)) - np.ones((k, m))

    def clone_without_children(self):
        node = KTreeNode(self.value, self.m, self.k)
        node.count = self.count
        node.pe = self.pe
        node.pms = self.pms
        node.Bs = self.Bs
        return node

    def graphviz(self):
        return [
            ("pe", "pe", graphviz.str_fraction),
            ("as", "count", None),
            ("pms", "pms", None),
            ("Bs", "Bs", graphviz.str_matrix)
        ]


def build_full_tree(m, k, D):
    def build_node(value, m, k, depth_to_go):
        node = KTreeNode(value, m, k)
        if depth_to_go != 0:
            children = list(build_node(i, m, k, depth_to_go - 1)
                            for i in range(m))
            node.children = children
        return node
    return build_node(None, m, k, D - 1)


def build_matrix(node, m, k, D, beta):  # returns the kj
    if node.is_leaf():
        node.pms[0] = node.pe
        node.Bs[0] = np.zeros((1, m))
        return 1
    else:
        kjs = [build_matrix(c, m, k, D, beta) for c in node.children]
        kj = min(kjs)

        probas = [(beta * node.pe, np.zeros((1, m)))]
        for ijs in ij_iterator(kj, m):
            p = (1 - beta) * \
                tree.product(node.children[j].pms[ijs[j] - 1]
                             for j in range(m))
            probas.append((p, np.array(ijs)))
        # sort by proba in desc order
        probas.sort(key=lambda p: p[0], reverse=True)
        kprobas = probas[:k]
        # print(probas, file=sys.stderr)
        for i, p in enumerate(kprobas):  # we only keep k of them
            node.Bs[i] = p[1]
            node.pms[i] = p[0]
        # assert node.Bs.shape == (k, m)
        return min(k, kj + 1)


def extract_tree(node, ki):
    row = node.Bs[ki]
    new_node = node.clone_without_children()
    if all(elem == 0 for elem in row):
        return new_node
    else:
        new_children = list(extract_tree(c, int(r) - 1)
                            for c, r in zip(node.children, row))
        new_node.children = new_children
        return new_node


def main(data, m, D, k, beta):
    print("Building full tree", file=sys.stderr)
    top = build_full_tree(m, k, D)
    print("Building counts", file=sys.stderr)
    tree.build_counts(top, data, D, None)
    print("Computing probas", file=sys.stderr)
    top.compute_probas(beta)
    print("Building matrix", file=sys.stderr)
    build_matrix(top, m, k, D, beta)
    # print(graphviz_ktree.main_node_to_graphviz(top))
    for score in range(k):
        print("Extracting tree {}".format(score), file=sys.stderr)
        best_tree = extract_tree(top, score)
        print(graphviz.main_node_to_graphviz(best_tree))


def test():
    kj = 4
    m = 3
    for i in ij_iterator(kj, m):
        print(i)


path = "../dataprojet2.txt"

# input_bits = [0, 1, 2, 2, 1, 0]
# input_bits=[0,1,0,1,1,1,0,1,0,1,0,1,0,1]

# input_bits = [2, 0, 1, 0, 2, 1, 1, 0, 2, 0, 1, 0, 2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2,
              2, 0, 0, 0, 1, 0, 2, 1, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 1, 1, 0, 2]
# input_bits = markov.gen_markov(5000)
data = Data(path)
main(data.data, m=data.m, D=9, k=3, beta=0.5)
