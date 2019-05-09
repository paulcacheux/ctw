from fractions import Fraction
import markov
import graphviz

class Tree:
    def __init__(self, m):
        self.m = m
        self.top = Node(None, 0, None, [], m)
        self.nodes = [self.top]
    
    def insert_node(self, value, depth, parent):
        node = Node(value, depth, parent, [], m)
        self.nodes.append(node)
        return node
    
    def get_node_of_depth(self, depth):
        return [node for node in self.nodes if node.depth == depth]

    def debug_print(self):
        for node in self.nodes:
            print("{}".format(repr(node)))
        
    def compute_prob(self, beta):
        for node in self.nodes:
            node.compute_pe()
        self.top.compute_pw(beta)
    
class Node:
    def __init__(self, value, depth, parent, children, m):
        self.m = m
        self.value = value
        self.depth = depth
        self.parent = parent
        self.children = children
        self.count = [0] * m
        self.pe = None
    
    def __repr__(self):
        return "Node(depth={}, value={}, context={}, count={}, pe={}, pw={})".format(self.depth, self.value, self.get_context(), self.count, float(self.pe), float(self.pw))
    
    def get_context(self):
        if self.parent is None:
            return []
        return [self.value] + self.parent.get_context()
    
    def compute_pe(self):
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
    
    def compute_pw(self, beta):
        if len(self.children) == 0:
            self.pw = self.pe
        else:
            p = 1
            for c in self.children:
                c.compute_pw(beta)
                p *= c.pw
            self.pw = beta * self.pe + (1 - beta) * p

    
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

m = 2
tree = Tree(m)
input_bits = markov.gen_markov(100)
build_tree(tree, input_bits, 3)
tree.compute_prob(Fraction(1, 2))
# tree.debug_print()

print(graphviz.main_node_to_graphviz(tree.top))