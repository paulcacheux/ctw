import prob_tree
import markov
from fractions import Fraction
import sys
import tree_gen

N = 5000
input_bits = markov.gen_markov(N)
m = 3
D = 6
beta = Fraction(3, 4)
# print(input_bits, file=sys.stderr)
tree = prob_tree.prune_tree_main(input_bits, m, D, beta)
gen = tree_gen.TreeGenerator(tree)
next_bits = []
for _ in range(N):
    next_bits.append(gen.next())
# print(next_bits, file=sys.stderr)
next_tree = prob_tree.prune_tree_main(next_bits, m, D, beta)