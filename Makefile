all: ktree

ktree: tree.svg

tree.svg: tree.dot
	dot tree.dot -o tree.svg -Tsvg

tree.dot: kTree.py
	python3 kTree.py > tree.dot

clean:
	rm tree.dot tree.svg