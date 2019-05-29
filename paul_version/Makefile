all: ktree

ktree: ktrees.svg
prob_tree: prune_tree.svg


ktrees.svg: ktrees.dot
	dot ktrees.dot | gvpack -g | dot -o ktrees.svg -Tsvg

ktrees.dot: kTree.py graphviz.py tree.py
	python3 kTree.py > ktrees.dot

prune_tree.svg: prune_tree.dot
	dot prune_tree.dot -o prune_tree.svg -Tsvg

prune_tree.dot: prob_tree.py graphviz.py tree.py
	python3 prob_tree.py > prune_tree.dot

clean:
	rm *.dot *.svg