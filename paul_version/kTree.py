# -*- coding: utf-8 -*-

from fractions import Fraction
import markov
import graphviz_ktree
import numpy as np
import sys


def product(iter):
    res = Fraction(1, 1)
    for elem in iter:
        res *= elem
    return res


def ij_iterator(kj, m):
    r = range(1, kj + 1)
    if m == 1:
        for i in r:
            yield (i,)
    else:
        for left in ij_iterator(kj, m - 1):
            for i in r:
                yield (*left, i)


class Node:
    def __init__(self, value, m, k):
        self.m = m
        self.k = k
        self.value = value
        self.children = [None] * m
        self.count = [0] * m
        self.pe = None
        self.pms = [0] * k
        self.Bs = np.zeros((k, m)) - np.ones((k, m))

    def __repr__(self):
        return "Node(depth={}, value={}, context={}, count={}, pe={})".format(self.depth, self.value, self.get_context(), self.count, float(self.pe))

    def clone_without_children(self):
        node = Node(self.value, self.m, self.k)
        node.count = self.count
        node.pe = self.pe
        node.pms = self.pms
        node.Bs = self.Bs
        return node

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


def build_full_tree(m, k, D):
    def build_node(value, m, k, depth_to_go):
        node = Node(value, m, k)
        if depth_to_go != 0:
            children = list(build_node(i, m, k, depth_to_go - 1)
                            for i in range(m))
            node.children = children
        return node
    return build_node(None, m, k, D - 1)


def build_counts(top_node, data, D):
    for width in range(1, D+1):
        for start in range(len(data) - width + 1):
            context = data[start:start+width]
            value = context[-1]
            pre = context[:-1]
            insert_node = top_node
            for c in reversed(pre):
                insert_node = insert_node.children[c]
            insert_node.count[value] += 1


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
                product(node.children[j].pms[ijs[j] - 1] for j in range(m))
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


"""
def complex_build_matrix(node, m, k, D, beta): # returns the kj
    if node.is_leaf():
        node.pms[0] = node.pe
        node.Bs[0] = np.zeros((1, m))
        return 1
    else:
        kj = None
        for c in node.children:
            kj = build_matrix(c, m, k, D, beta)
        # if kj == 1:
        #     left = beta * node.pe
        #     right = (1 - beta) * product(c.pms[0] for c in node.children)
        #     probas = [(left, np.zeros((1, m))), (right, np.ones((1, m)))]
        #     probas.sort(key=lambda p:p[0], reverse=True)
        #     node.pms[0] = probas[0][0]
        #     node.pms[1] = probas[1][0]
        #     node.Bs[0] = probas[0][1]
        #     node.Bs[1] = probas[1][1]
        #     return 2
        # else:
        probas = [(beta * node.pe, np.zeros((1, m)))]
        for ijs in ij_iterator(kj, m):
            p = (1 - beta) * product(node.children[j].pms[ijs[j] - 1] for j in range(m))
            probas.append((p, np.array(ijs)))
        probas.sort(key=lambda p:p[0], reverse=True) # sort by proba in desc order
        kprobas = probas[:k]
        # print(probas, file=sys.stderr)
        for i, p in enumerate(kprobas): # we only keep k of them
            node.Bs[i] = p[1]
            node.pms[i] = p[0]
        # assert node.Bs.shape == (k, m)
        return min(k, kj + 1)
"""


def main(data, m, D, k, beta):
    print("Building full tree", file=sys.stderr)
    top = build_full_tree(m, k, D)
    print("Building counts", file=sys.stderr)
    build_counts(top, input_bits, D)
    print("Computing probas", file=sys.stderr)
    top.compute_probas(beta)
    print("Building matrix", file=sys.stderr)
    build_matrix(top, m, k, D, beta)
    # print(graphviz_ktree.main_node_to_graphviz(top))
    for score in range(k):
        print("Extracting tree {}".format(score), file=sys.stderr)
        best_tree = extract_tree(top, score)
        print(graphviz_ktree.main_node_to_graphviz(best_tree))


def test():
    kj = 4
    m = 3
    for i in ij_iterator(kj, m):
        print(i)


def read_input(path):
    res = []
    with open(path) as f:
        for line in f:
            for c in line:
                if c.isdigit():
                    res.append(int(c))
    return res


path = "../dataprojet2.txt"

# input_bits = [0, 1, 2, 2, 1, 0]
# input_bits=[0,1,0,1,1,1,0,1,0,1,0,1,0,1]
# input_bits = markov.gen_markov(5000)
input_bits = read_input(path)
main(input_bits, m=5, D=9, k=3, beta=0.5)
