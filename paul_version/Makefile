.PHONY: clean_output ktree prob_tree markov_tester
all: ktree prob_tree markov_tester

ktree: output/ktrees.svg
prob_tree: output/prune_tree.svg
markov_tester: output/markov_tester.svg

output/%.svg: output/%.dot
	dot $< | gvpack -g | dot -o $@ -Tsvg

output/ktrees.dot: kTree.py graphviz.py tree.py
	python3 kTree.py > $@

output/prune_tree.dot: prob_tree.py graphviz.py tree.py
	python3 prob_tree.py > $@

output/markov_tester.dot: markov_tester.py graphviz.py tree.py
	python3 markov_tester.py > $@

clean_output:
	rm output/*.dot output/*.svg