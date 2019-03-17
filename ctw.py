import random
import sys

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
        print(tab + "Node(value={}, count={})".format(self.value, self.count))
        for c in self.children:
            if c != None:
                c.pretty_print(depth + 1)

    def predict(self, suffix):
        current_pred = self.count.index(max(self.count))
        if len(suffix) == 0:
            return current_pred
        else:
            last = suffix[-1]
            rest = suffix[:-1]
            next_node = self.children[last]
            if next_node != None:
                return next_node.predict(rest)
            else:
                return current_pred


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

    start_pred = "pri"
    next_words = data.convert_to_indexes(start_pred)
    for _ in range(20000):
        next_word = node.predict(next_words)
        next_words.append(next_word)

    next_words = data.convert_to_text(next_words)
    print(next_words)

def main_bits():
    # input_bits = [0, 1, 2, 3, 2, 1] * 3;
    input_bits = [random.randrange(4) for _ in range(40)]
    node = build_ctw(input_bits, 3, 4)
    Node.pretty_print(node)

    next_bits = []
    for _ in range(20):
        next_bit = node.predict(input_bits + next_bits)
        next_bits.append(next_bit)

    print(next_bits)

if __name__ == "__main__":
    main_text()

