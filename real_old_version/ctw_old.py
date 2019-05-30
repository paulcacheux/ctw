import random
import sys
import graphviz

def product(iterator):
    res = 1
    for i in iterator:
        res *= i
    return res

def max_predictor(array):
    assert len(array) != 0
    index = 0
    max_value = None
    for (i, value) in enumerate(array):
        if max_value is None or value > max_value:
            max_value = value
            index = i
    return index

def random_predictor(array):
    assert len(array) != 0
    indexes = list(range(len(array)))
    res = random.choices(indexes, weights=array)
    return res[0]


class TextConvertData:
    def __init__(self, text):
        words = []
        indexes = []
        for word in text:
            try:
                i = words.index(word)
                indexes.append(i)
            except ValueError:
                indexes.append(len(words))
                words.append(word)
        self.words = words
        self.indexes = indexes
        self.max = len(indexes)

    def convert_to_indexes(self, text):
        return [self.words.index(w) for w in text] # exeeption if not in given letters

    def convert_to_text(self, indexes):
        return "".join(self.words[i] for i in indexes)
    

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
        print(tab + "Node(value={}, count={}, pe={}, pw={})".format(self.value, self.count, self.pe, self.pw))
        for c in self.children:
            if c != None:
                c.pretty_print(depth + 1)

    def predict(self, suffix, predictor):
        if len(suffix) != 0:
            last = suffix[-1]
            rest = suffix[:-1]
            next_node = self.children[last]
            if next_node != None:
                return next_node.predict(rest, predictor)
        
        return predictor(self.count)
    
    def compute_pe(self):
        res = product(i + 0.5 for j in range(self.N) for i in range(self.count[j]))
        M = sum(self.count)
        for i in range(M):
            res /= (self.N / 2 + i)
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

    def compute_proba(self, beta):
        for c in self.children:
            if c is not None:
                c.compute_proba(beta)
        
        self.compute_pe()
        self.compute_pw(beta)
        self.compute_pm(beta)
    
    def prune(self, beta):

    

def build_ctw(input_bytes, mem_size, N):
    node = Node(N)
    suffix_size = mem_size + 1
    for i in range(len(input_bytes) - suffix_size + 1):
        suffix, then = input_bytes[i:i+mem_size], input_bytes[i + mem_size]
        # print("adding : ({} -> {})".format(suffix, then))
        node.add_suffix(suffix, then)
    return node

def main_text():
    path = sys.argv[1]
    text = open(path).read()
    data = TextConvertData(text)
    indexes = data.indexes
    mem_size = 10
    node = build_ctw(indexes, mem_size, data.max)
    # Node.pretty_print(node)
    predictor = random_predictor

    start_pred = "pri"
    next_words = data.convert_to_indexes(start_pred)
    for _ in range(2000):
        next_word = node.predict(next_words, predictor)
        next_words.append(next_word)

    next_words = data.convert_to_text(next_words)
    print(next_words)

def main_bits():
    input_bits = [0, 1, 2, 3, 2, 1] * 3
    # input_bits = [random.randrange(4) for _ in range(40)]
    node = build_ctw(input_bits, 3, 4)
    node.compute_proba(0.5)
    Node.pretty_print(node)
    print(graphviz.main_node_to_graphviz(node))

    next_bits = []
    for _ in range(20):
        next_bit = node.predict(input_bits + next_bits, max_predictor)
        next_bits.append(next_bit)

    print(next_bits)

if __name__ == "__main__":
    main_bits()

