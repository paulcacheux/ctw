all: ktree

ktree: trees.svg

trees.svg: trees.dot
	dot trees.dot | gvpack -g | dot -o trees.svg -Tsvg

trees.dot: kTree.py graphviz_ktree.py
	python3 kTree.py > trees.dot

clean:
	rm trees.dot trees.svg