class GraphvizDrawer:
    def __init__(self):
        self.counter = 0
        self.s = "digraph nodes {\n\tnode [shape=record];\n"

    def next_name(self):
        i = self.counter
        self.counter += 1
        return "name{}".format(i)

    def draw_node(self, node):
        name = self.next_name()
        fmt = "\t{} [label=\"{{".format(name)
        elems = []
        for (attr_name, attr, func) in node.graphviz():
            value = getattr(node, attr)
            if func is not None:
                value = func(value)
            elems.append("{}={}".format(attr_name, value))
        fmt += " | ".join(elems)
        fmt += "}}\"];\n"
        self.s += fmt

        for c in node.children:
            if c is not None:
                sub_name = self.draw_node(c)
                self.s += "\t{} -> {} [label={}];\n".format(
                    name, sub_name, c.value)
        return name

    def build(self):
        return self.s + "}\n"


def str_fraction(f):
    return float(f) if f else 0.0


def str_matrix(Bs):
    res = "\\n"
    for row in Bs:
        if all(elem == 0 for elem in row):
            res += "[{}]".format(", ".join(["*"] * len(row)))
        else:
            res += str(row)
        res += "\\n"
    return res


def main_node_to_graphviz(node):
    drawer = GraphvizDrawer()
    drawer.draw_node(node)
    return drawer.build()
