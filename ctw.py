import random
import sys
import graphviz
import markov
from fractions import Fraction

def product(iterator):
    res = 1
    for i in iterator:
        res *= i
    return res

class Node:
    def __init__(self, N, value=None):
        self.N = N
        self.value = value
        self.count = [0] * N
        self.children = [None] * N

    def is_leaf(self):
        return all(c is None for c in self.children)

    def add_suffix(self, suffix, then):
        if len(suffix) == 0:
            return

        last = suffix[-1]
        rest = suffix[:-1]

        if self.children[last] == None:
            self.children[last] = Node(self.N, last)

        self.children[last].count[then] += 1
        self.children[last].add_suffix(rest, then)

    def pretty_print(self, depth=0):
        tab = "\t" * depth
        print(tab + "Node(value={}, count={}, pe={}, pw={}, pm={})".format(self.value, self.count, self.pe, self.pw, self.pm))
        for c in self.children:
            if c != None:
                c.pretty_print(depth + 1)
    
    def compute_pe(self):
        res = product(i + Fraction(1, 2) for j in range(self.N) for i in range(self.count[j]))
        M = sum(self.count)
        for i in range(M):
            coeff = Fraction(self.N, 2) + i
            res /= coeff
        self.pe = res
    
    def compute_pw(self, beta):
        if self.is_leaf():
            self.pw = self.pe
        else:
            prod = product(c.pw for c in self.children if c is not None)
            self.pw = beta * self.pe + (1 - beta) * prod
    
    def compute_pm(self, beta):
        if self.is_leaf():
            self.pm = self.pe
        else:
            prod = product(c.pm for c in self.children if c is not None)
            inv_beta_prod = (1 - beta) * prod
            self.pm = max(beta * self.pe, inv_beta_prod)


    def compute_proba(self, beta):
        for c in self.children:
            if c is not None:
                c.compute_proba(beta)
        
        self.compute_pe()
        self.compute_pw(beta)
        self.compute_pm(beta)
    
    def prune(self, beta):
        if self.pm == beta * self.pe:
            self.children = [None] * self.N
        else:
            for c in self.children:
                if c is not None:
                    c.prune(beta)


def build_ctw(input_bytes, mem_size, N):
    node = Node(N)
    suffix_size = mem_size + 1
    for i in range(len(input_bytes) - suffix_size + 1):
        suffix, then = input_bytes[i:i+mem_size], input_bytes[i + mem_size]
        # print("adding : ({} -> {})".format(suffix, then))
        node.add_suffix(suffix, then)
    return node

def main():
    # input_bits = [0, 1, 2, 3, 2, 1] * 3
    # input_bits = [random.randrange(4) for _ in range(40)]
    input_bits = markov.gen_markov(10000)
    # input_bits = [0, 0] + [1, 1, 0, 0, 1, 0, 1, 0, 1, 0]
    # input_bits = [0, 0] + [0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1]
    # print(input_bits)
    node = build_ctw(input_bits, 4, 2)
    beta = 0.5
    node.compute_proba(beta)
    # node.prune(beta)
    # Node.pretty_print(node)
    print(graphviz.main_node_to_graphviz(node))

if __name__ == "__main__":
    main()

