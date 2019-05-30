.PHONY: clean_output ktree prob_tree markov_tester
all: ktree prob_tree markov_tester

ktree: output/ktrees.html
prob_tree: output/prune_tree.svg
markov_tester: output/markov_tester.svg

output/%.svg: output/%.gv
	dot $< | gvpack -g | dot -o $@ -Tsvg

output/%.svg: output/%.dot
	dot $< -o $@ -Tsvg

output/ktrees.html: kTree.py graphviz.py tree.py
	python3 kTree.py html > $@

output/prune_tree.dot: prob_tree.py graphviz.py tree.py
	python3 prob_tree.py > $@

output/markov_tester.gv: markov_tester.py graphviz.py tree.py
	python3 markov_tester.py > $@

clean_output:
	rm output/*.dot output/*.svg