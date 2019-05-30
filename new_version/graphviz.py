class GraphvizDrawer:
    def __init__(self):
        """Constructs a new Drawer.
        """
        self.counter = 0
        self.s = "digraph nodes {\n\tnode [shape=record];\n"

    def next_name(self):
        """Get a new unique node name.
        Returns:
            string: a new unique node name.
        """
        i = self.counter
        self.counter += 1
        return "name{}".format(i)

    def add_node(self, name, label):
        """Add a node to the graph.
        Params:
            name (string): the name of the node.
            label (string): the label of the node.
        """
        self.s += "\t{} [label=\"{}\"];\n".format(name, label)
    
    def add_edge(self, node1, node2, label):
        """Add an edge to the graph.
        Params:
            node1 (string): the name of the first node.
            node2 (string): the name of the second node.
            label (string): the label of the edge.
        """
        self.s += "\t{} -> {} [label={}];\n".format(node1, node2, label)

    def add_tree_node(self, node):
        """Add a tree node to the graph.
        Params:
            node (Node): node to add to the graph.
        Returns:
            string: the name of the node added (to build edges).
        """

        def build_label(node):
            """Build the label according to the node graphviz description"""
            label = "{"
            elems = []
            for (attr_name, attr, func) in node.graphviz():
                value = getattr(node, attr)
                if func is not None:
                    value = func(value)
                elems.append("{}={}".format(attr_name, value))
            label += " | ".join(elems)
            label += "}"
            return label

        name = self.next_name()
        label = build_label(node)
        self.add_node(name, label)

        for c in node.children:
            if c is not None:
                sub_name = self.add_tree_node(c)
                self.add_edge(name, sub_name, c.value)
        return name

    def build(self):
        """End drawing and build final string
        Returns:
            string: the graphviz description of the graph.
        """
        return self.s + "}\n"

def str_fraction_array(arr):
    """Utility fonction to print fraction arrays."""
    return [str_fraction(elem) for elem in arr]

def str_fraction(f):
    """Utility fonction to print fractions."""
    return float(f) if f else 0.0

def str_matrix(Bs):
    """Utility fonction to print matrix (mainly Bs)."""
    res = "\\n"
    for row in Bs:
        if all(elem == 0 for elem in row):
            res += "[{}]".format(", ".join(["*"] * len(row)))
        else:
            res += str(row)
        res += "\\n"
    return res


def main_node_to_graphviz(node):
    """Get graphviz description of a node tree
    Args:
        node (Node): the top node of the tree.
    Returns:
        string: The graphviz description of the tree.
    """
    drawer = GraphvizDrawer()
    drawer.add_tree_node(node)
    return drawer.build()
