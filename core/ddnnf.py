from collections import namedtuple

LNODE = namedtuple("LNODE", "node_type node_field")


class DDNNF:
    """

    Assumption:
        Bottom-up structure (i.e., each node is preceded by its children)
        There is one root node, and it is the last node.
        Variables (1-n) make up the first nodes.

        node_field is indexed from 1 (because can not negate 0)
        to avoid confusion, we add a dummy node.
    """
    def __init__(self):
        self.nodes = [LNODE("dummy", "")]  # type: list[LNODE]
        self.var_count = 0

    def add_node(self, node_type: str, node_field):
        """
        Add a node to this d-DNNF.
        :param node_type: The type of the node. Either atom, conj or disj
        :param node_field: If conj or disj, this should be a list/tuple of children.
            Each indexed from 1, and using -l to denote negation of l.
            If atom, no restrictions apply
        :return:
        """
        assert node_type == "atom" or node_type == "conj" or node_type == "disj"
        self.nodes.append(LNODE(node_type, node_field))
        if node_type == "atom":
            self.var_count += 1
        return len(self.nodes) - 1

    def add_atom(self, node_field):
        return self.add_node("atom", node_field)

    def add_conj(self, children):
        return self.add_node("conj", children)

    def add_disj(self, children):
        return self.add_node("disj", children)

    def is_bottom_up(self):
        """ This should be true unless an assumption is violated (cf. class description) """
        for index, node in enumerate(self):
            if node.node_type == "conj" or node.node_type == "disj":
                children = node.node_field
                if any((abs(child_index) > index) for child_index in children):
                    return False
        return True

    def __iter__(self):
        for idx, node in enumerate(self.nodes[1:]):
            yield idx+1, node

    def __getitem__(self, item):
        return self.nodes.__getitem__(item)


class FormulaOverlayList:
    """
        Useful to store information for each formula node.

        #TODO Add usage example
    """

    def __init__(self, ddnnf, default_constructor=None):
        super().__init__()
        self.ddnnf = ddnnf
        if default_constructor is None:
            self.overlay = [None] * len(ddnnf.nodes)
        else:
            self.overlay = [default_constructor(index, node) for (index, node) in ddnnf.nodes]

    def __iter__(self):
        yield from self.overlay.__iter__()

    def __getitem__(self, item: int):
        return self.overlay[item]

    def __setitem__(self, key: int, value):
        self.overlay[key] = value


def ddnnf_to_dot(ddnnf, prop_function=None) -> str:
    """Write out in GraphViz (dot) format.
    :param ddnnf: to create dot representation of.
    :prop_function: function taking node_index, node and returning additional node properties
    :return: string containing dot representation
    """
    if prop_function is None:
        prop_function = lambda i, n: ""

    s = "digraph GP {\n"
    for index, node in ddnnf:
        nprop = prop_function(index, node)
        if nprop == "":
            nprop = 'fillcolor="white"'
        nprop = ", " + nprop
        if node.node_type == "atom":
            s += f'{index} [label="{index}", shape="box", style="filled"{nprop}];\n'
        elif node.node_type == "conj":
            children = node.node_field
            s += f'{index} [label="&and;", shape="circle", style="filled"{nprop}];\n'
            for child_idx in children:
                neg_label = '[arrowhead="normal", dir="both", arrowtail="odot"]' if child_idx < 0 else ""
                s += f"{index} -> {abs(child_idx)}{neg_label}\n"
        elif node.node_type == "disj":
            children = node.node_field
            s += f'{index} [label="&or;", shape="circle", style="filled"{nprop}];\n'
            for child_idx in children:
                neg_label = '[arrowhead="normal", dir="both", arrowtail="odot"]' if child_idx < 0 else ""
                s += f"{index} -> {abs(child_idx)}{neg_label}\n"
        else:
            raise TypeError(f"Unexpected node type: {node.node_type}")
    return s + "}"
