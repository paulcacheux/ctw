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
        self.s += '\t{} [label="pe={:.3f} | pw={:.3f} | as={}"];\n'.format(name, float(node.pe), float(node.pw), node.count)
        for c in node.children:
            if c is not None:
                sub_name = self.draw_node(c)
                self.s += "\t{} -> {} [label={}];\n".format(name, sub_name, c.value)
        return name
        
    def build(self):
        return self.s + "}\n"

def main_node_to_graphviz(node):
    drawer = GraphvizDrawer()
    drawer.draw_node(node)
    return drawer.build()
