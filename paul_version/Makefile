.PHONY: clean ktree prob_tree
all: ktree prob_tree markov_tester

ktree: ktrees.svg
prob_tree: prune_tree.svg
markov_tester: markov_tester.svg

ktrees.svg: ktrees.dot
	dot ktrees.dot | gvpack -g | dot -o ktrees.svg -Tsvg

ktrees.dot: kTree.py graphviz.py tree.py
	python3 kTree.py > ktrees.dot

prune_tree.svg: prune_tree.dot
	dot prune_tree.dot -o prune_tree.svg -Tsvg

prune_tree.dot: prob_tree.py graphviz.py tree.py
	python3 prob_tree.py > prune_tree.dot

markov_tester.svg: markov_tester.dot
	dot markov_tester.dot | gvpack -g | dot -o markov_tester.svg -Tsvg

markov_tester.dot: markov_tester.py graphviz.py tree.py
	python3 markov_tester.py > markov_tester.dot

clean:
	rm *.dot *.svg