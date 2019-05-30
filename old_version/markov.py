import random

class MarkovGen:
    def __init__(self):
        self.trans = {}
        self.trans[(0, 0)] = [0.3,0.6,0.1]
        self.trans[(0, 1)] = [0,0,1]
        self.trans[(1, 0)] = [0.3,0.6,0.1]
        self.trans[(1, 1)] = [1, 0, 0]
        self.trans[(0, 2)] = [0.2, 0.7, 0.2]
        self.trans[(2, 0)] = [0.3, 0.4 ,0.3]
        self.trans[(1, 2)] = [0.3, 0.5 ,0.2]
        self.trans[(2, 1)] = [0 ,0.8 ,0.2]
        self.trans[(2, 2)] = [0.1 ,0 ,0.9]
        self.mem = [0, 0]
    
    def next(self):
        prob0 = self.trans[(self.mem[-1], self.mem[-2])][0]
        prob1 = self.trans[(self.mem[-1], self.mem[-2])][1]
        n = 0
        val=random.random()
        if val < prob0:
            n = 0
        elif prob0 < val < prob1+prob0 :
            n = 1
        else : 
            n = 2
            
        self.mem = [self.mem[-1], n]
        return n
    

def gen_markov(n):
    res = []
    g = MarkovGen()
    for i in range(n):
        res.append(g.next())
    return res