import random

class MarkovGen:
    def __init__(self):
        self.trans = {}
        self.trans[(0, 0)] = 0.8
        self.trans[(0, 1)] = 0.5
        self.trans[(1, 0)] = 0.5
        self.trans[(1, 1)] = 0.0
        self.mem = [0, 0]
    
    def next(self):
        prob = self.trans[(self.mem[-1], self.mem[-2])]
        n = 0
        if random.random() < prob:
            n = 1
        self.mem = [self.mem[-1], n]
        return n
    

def gen_markov(n):
    res = []
    g = MarkovGen()
    for i in range(n):
        res.append(g.next())
    return res