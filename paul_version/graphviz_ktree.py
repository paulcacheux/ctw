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
        pe = float(node.pe) if node.pe else 0.0
        self.s += '\t{} [label="{{pe={:.3f} | as={} | pms={} | bs=\\n{}}}"];\n'.format(name, pe, node.count, node.pms, str_matrix(node.Bs))
        for c in node.children:
            if c is not None:
                sub_name = self.draw_node(c)
                self.s += "\t{} -> {} [label={}];\n".format(name, sub_name, c.value)
        return name
        
    def build(self):
        return self.s + "}\n"

def str_matrix(Bs):
    res = ""
    for row in Bs:
        if all(elem == 0 for elem in row):
            res += str(list("*" for _ in row))
        else:
            res += str(row)
        res += "\\n"
    return res

def main_node_to_graphviz(node):
    drawer = GraphvizDrawer()
    drawer.draw_node(node)
    return drawer.build()
