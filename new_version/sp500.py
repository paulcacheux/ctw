import prob_tree
import kTree
import csv
from fractions import Fraction
import graphviz
import tree

path = "./input_data/GSPC.csv"
data = []
with open(path) as f:
    reader = csv.DictReader(f)
    for row in reader:
        data.append(float(row["Adj Close"]))

diff = []
for (a, b) in zip(data, data[1:]):
    diff.append(b / a * 100 - 100)

res = []
for d in diff:
    v = None
    if d <= -5:
        v = 0
    elif -5 < d and d <= -3:
        v = 1
    elif -3 < d and d <= -1:
        v = 2
    elif -1 < d and d <= 1:
        v = 3
    elif 1 < d and d <= 3:
        v = 4
    elif 3 < d and d <= 5:
        v = 5
    elif d > 5:
        v = 6
    res.append(v)

alphabet_size = 7
tree_depth = 6
beta = Fraction(1, 2)

top = prob_tree.prune_tree_main(res, alphabet_size, tree_depth, beta)
print(float(top.compute_pi_T_x(beta, tree_depth, top.pw)))

# print(graphviz.main_node_to_graphviz(top))