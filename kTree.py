# -*- coding: utf-8 -*-
"""
Created on Thu May  9 18:24:31 2019

@author: Mathurin
"""

from fractions import Fraction
import markov
import graphviz_ktree
import numpy as np

def product(iter):
    res = 1
    for elem in iter:
        res *= elem
    return res

def ij_iterator(kj, m):
    if m == 1:
        for i in range(kj):
            yield (i,)
    else:
        for left in ij_iterator(kj, m - 1):
            for i in range(kj):
                yield (*left, i)

class Tree:
    def __init__(self, m, k):
        self.m = m
        self.top = Node(None, 0, None, [], m, k)
        self.nodes = [self.top]
    
    def insert_node(self, value, depth, parent, k):
        node = Node(value, depth, parent, [], self.m, k)
        self.nodes.append(node)
        return node
    
    def get_node_of_depth(self, depth):
        return [node for node in self.nodes if node.depth == depth]

    def debug_print(self):
        for node in self.nodes:
            print("{}".format(repr(node)))
        
    def compute_prob(self):
        for node in self.nodes:
            node.compute_pe()
    
class Node:
    def __init__(self, value, depth, parent, children, m, k):
        self.m = m
        self.value = value
        self.depth = depth
        self.parent = parent
        self.children = children
        self.count = [0] * m
        self.pe = None
        self.pms = [0] * k
        self.Bs = np.zeros((k, m)) - np.ones((k, m))
    
    def __repr__(self):
        return "Node(depth={}, value={}, context={}, count={}, pe={}, pw={})".format(self.depth, self.value, self.get_context(), self.count, float(self.pe), float(self.pw))
    
    def is_leaf(self):
        return len(self.children)==0
    
    def get_context(self):
        if self.parent is None:
            return []
        return [self.value] + self.parent.get_context()
    
    def compute_pe(self):
        Ms = sum(self.count)
        if Ms == 0:
            self.pe = Fraction(1, 1)
            return

        num = 1
        for j in range(self.m):
            for i in range(self.count[j]):
                num *= Fraction(1, 2) + i
        
        den = 1
        for i in range(Ms):
            den *= Fraction(self.m, 2) + i
        
        res = num / den
        self.pe = res

def build_full_tree(tree, m, D, k):
    for depth in range(0, D):
        for node in tree.get_node_of_depth(depth):
            for value in range(m):
                value_node = get_node_in_tree(tree, node, depth, value, k)

    
def build_tree(tree, data, D, k):
    for i in range(1, D+1):
        for j in range(len(data) - i + 1):
            context = data[j:j+i]
            value = context[0]
            rest = context[1:]
            depth = len(rest)
            after = None
            if j+i < len(data):
                after = data[j+i]

            for node in tree.get_node_of_depth(depth):
                if node.get_context() == rest:
                    value_node = get_node_in_tree(tree, node, depth, value, k)
                    if after is not None:
                        value_node.count[after] += 1

def build_matrix(tree, k, D, beta):
    m = tree.m
    depth = D - 1
    for node in tree.get_node_of_depth(depth):
        node.pms[0] = node.pe
        node.Bs[0] = np.zeros((1, m))

    depth = D - 2
    for node in tree.get_node_of_depth(depth):
        left = beta * node.pe
        right = (1 - beta) * product(c.pms[0] for c in node.children)
        if left > right:
            node.pms[0] = left
            node.Bs[0] = np.zeros((1, m))
            node.Bs[1] = np.ones((1, m))
        else:
            node.pms[1] = right
            node.Bs[1] = np.zeros((1, m))
            node.Bs[0] = np.ones((1, m))
    for depth in range(3, D):
        depth = D - depth
        probas = [(beta * node.pe, np.zeros((1, m)))]
        kj = D - depth
        for ijs in ij_iterator(kj, m):
            p = (1 - beta) * product(node.children[j].pms[ijs[j]] for j in range(m))
            probas.append((p, np.array(ijs)))
        probas.sort(key=lambda p:p[0], reverse=True) # sort by proba in desc order
        probas = probas[:k] # we keep only k of them
        node.Bs = np.array(probas[1])
        node.pms = list(p[0] for p in probas)
        # assert node.Bs.shape == (k, m)


def get_node_in_tree(tree, current_node, depth, value, k):
    for c in current_node.children:
        if c.value == value:
            return c
    c = tree.insert_node(value, depth + 1, current_node, k)
    current_node.children.append(c)
    return c

def compute_input_proba(tree):
    proba=1
    for node in tree.nodes :
        if node.is_leaf():      # le noeud est une feuille
            proba*=node.pe
    return proba


def main():
    m = 3
    D = 4
    k = 3
    tree = Tree(m, k)
    #input_bits = markov.gen_markov(10)
    input_bits=[0,1,0,1,0,1,0,1,0,1,0,1,0,1]
    # print(input_bits)
    build_full_tree(tree, m, D, k)
    build_tree(tree, input_bits, D, k)
    tree.compute_prob()
    build_matrix(tree, k, D, 0.5)
    print(graphviz_ktree.main_node_to_graphviz(tree.top))

def test():
    for i in ij_iterator(2, 3):
        print(i)

main()