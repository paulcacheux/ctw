# -*- coding: utf-8 -*-
"""
Created on Thu May  9 18:24:31 2019

@author: Mathurin
"""

from fractions import Fraction
import markov
import graphviz_ktree
import numpy as np

class Tree:
    def __init__(self, m, k):
        self.m = m
        self.top = Node(None, 0, None, [], m)
        self.nodes = [self.top]
    
    def insert_node(self, value, depth, parent, k):
        node = Node(value, depth, parent, [], m, k)
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
            den *= Fraction(m, 2) + i
        
        res = num / den
        self.pe = res

def build_full_tree(tree, m, D):
    for depth in range(0, D):
        for node in tree.get_node_of_depth(depth):
            for value in range(m):
                value_node = get_node_in_tree(tree, node, depth, value)

    
def build_tree(tree, data, D):
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
                    value_node = get_node_in_tree(tree, node, depth, value)
                    if after is not None:
                        value_node.count[after] += 1

def get_node_in_tree(tree, current_node, depth, value):
    for c in current_node.children:
        if c.value == value:
            return c
    c = tree.insert_node(value, depth + 1, current_node)
    current_node.children.append(c)
    return c

def compute_input_proba(tree):
    proba=1
    for node in tree.nodes :
        if node.is_leaf():      # le noeud est une feuille
            proba*=node.pe
    return proba

m = 3
D = 2
k = 3
tree = Tree(m, k)
#input_bits = markov.gen_markov(10)
input_bits=[0,1,0,1,0,1,0,1,0,1,0,1,0,1]
# print(input_bits)
build_full_tree(tree, m, D)
build_tree(tree, input_bits, D)
tree.compute_prob()
print(graphviz_ktree.main_node_to_graphviz(tree.top))

