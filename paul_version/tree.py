from fractions import Fraction
import graphviz


class Node:
    def __init__(self, value, m):
        """Constructs a Node to be used in a tree.

        Args:
            value (int|None): The value to be stored in this node.
            m (int): The alphabet size.
        """
        self.m = m
        self.value = value
        self.children = [None] * m
        self.count = [0] * m
        self.pe = None

    def is_leaf(self):
        """
        Returns:
            bool: True if the node is a leaf ie. if it has no children.
        """
        return all(c is None for c in self.children)

    def get_pe(self):
        """
        Returns:
            int: The Pe probability of this Node, calculated on demand. This value is not stored.
        """
        Ms = sum(self.count)
        if Ms == 0:
            return Fraction(1, 1)

        num = 1
        for j in range(self.m):
            for i in range(self.count[j]):
                num *= Fraction(1, 2) + i

        den = 1
        for i in range(Ms):
            den *= Fraction(self.m, 2) + i

        res = num / den
        return res

    def compute_probas(self, beta):
        """Compute all required probability on this Node. And store those values.
        Args:
            beta (int): The beta value used in some probabilities.
        """
        for c in self.children:
            if c is not None:
                c.compute_probas(beta)
        self.pe = self.get_pe()

    def graphviz(self):
        """Description of interesting fields of the Node to be used by Graphviz.
        Returns:
            [(string, string, T -> value)]:
                the first element is the field name to be display,
                the second element is the name of the field attr ("pe" would be used if you want self.pe),
                the third element is the function to be used to convert to string, or None if you want the default __str__().
        """
        return [
            ("pe", "pe", graphviz.str_fraction),
            ("as", "count", None)
        ]


def build_counts(top_node, data, D, node_builder):
    """Complete the counts vector using some input data.
    Args:
        top_node (Node): the top node of the tree.
        data ([int]): the input data.
        D (int): the context size.
        node_builder ((int, int) -> Node): a node builder used when inserting a Node is needed.
            It takes the value of the node and the alphabet size as parameters.
    """
    m = top_node.m
    for width in range(1, D+1):
        for start in range(len(data) - width + 1):
            context = data[start:start+width]
            value = context[-1]
            pre = context[:-1]
            insert_node = top_node
            for c in reversed(pre):
                # shouldn't append in kTree so we can build a Node and not a KTreeNode
                if insert_node.children[c] is None:
                    insert_node.children[c] = node_builder(c, m)
                insert_node = insert_node.children[c]
            insert_node.count[value] += 1


def product(iter):
    """Utility product function
    Args:
        iter ([Fraction]): the elements to be used
    Returns:
        Fraction: the product of all the elements of iter
    """
    res = Fraction(1, 1)
    for elem in iter:
        res *= elem
    return res
