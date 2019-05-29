# -*- coding: utf-8 -*-
"""
Created on Fri May 10 02:43:59 2019

@author: Mathurin
"""


from fractions import Fraction
import markov
import graphvize

class Tree:
    def __init__(self, m,beta):
        self.m = m
        self.beta=beta
        self.top = Node(None, 0, None, [], m)
        self.nodes = [self.top]
    
    def insert_node(self, value, depth, parent):
        node = Node(value, depth, parent, [],self.m)
        self.nodes.append(node)
        return node
    
    def get_node_of_depth(self, depth):
        return [node for node in self.nodes if node.depth == depth]

    def debug_print(self):
        for node in self.nodes:
            print("{}".format(repr(node)))
        
    def compute_pe(self):
        for node in self.nodes:
            node.compute_pe(self.m)
        self.top.compute_pe(self.m)
    
    def compute_pm(self):
        for node in self.nodes:
            node.compute_pm(self.beta)
        self.top.pm=self.top.pe
    
    def pruning(self):
        for node in self.nodes :
            if float(node.pe*self.beta)==float(node.pm) :
                node.delete_descendant(self)
    
    
class Node:
    def __init__(self, value, depth, parent, children, m):
        self.m = m
        self.value = value
        self.depth = depth
        self.parent = parent
        self.children = children
        self.count = [0] * m
        self.pe = None
        self.pm = None
    
    def __repr__(self):
        return "Node(depth={}, value={}, context={}, count={}, pe={}, pm={}, isleaf={})".format(self.depth, self.value, self.get_context(), self.count, float(self.pe), float(self.pm), self.is_leaf())
    
    def is_leaf(self):
        return len(self.children)==0
    
    def get_context(self):
        if self.parent is None:
            return []
        return [self.value] + self.parent.get_context()
    
    def compute_pe(self,m):
        Ms = sum(self.count)
        num = 1
        for j in range(self.m):
            for i in range(self.count[j]):
                num *= Fraction(1, 2) + i
        
        den = 1
        for i in range(Ms):
            den *= Fraction(m, 2) + i
        
        res = num / den
        self.pe = res
    
    def compute_pm(self, beta):
        if self.is_leaf():
            self.pm = self.pe
        else:
            p= 1
            for c in self.children:
                c.compute_pm(beta)
                p *= c.pm
            self.pm = max(beta * self.pe, (1 - beta) * p)
            
    def delete_descendant(self,tree):
        while len(self.children):
            self.children[0].delete_descendant(tree)
            tree.nodes.remove(self.children[0])
            self.children.remove(self.children[0])
            
            
    
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

def main(m,D,beta,input_bits):
    tree = Tree(m,beta)
    #print(input_bits)
    build_tree(tree, input_bits, D)
    tree.compute_pe()
    tree.compute_pm()
    tree.pruning()
   #tree.debug_print()
    print(graphvize.main_node_to_graphviz(tree.top))
 
input_bits = markov.gen_markov(10000)
#input_bits=[0, 1, 1, 0, 2, 0, 1, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 1, 1]
# input_bits=[2, 0, 1, 0, 2, 1, 1, 0, 2, 0, 1, 0, 2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1, 0, 2, 1, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 1, 1, 0, 2]    
main(3,3,Fraction(1,2),input_bits)