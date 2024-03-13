from collections import namedtuple

LNODE = namedtuple("LNODE", "node_type node_field")


class DDNNF:
    """

    Assumption:
        Bottom-up structure (i.e., each node is preceded by its children)
        There is one root node, and it is the last node.
        Variables (1-n) make up the first nodes.

        node_field is indexed from 1 (because can not negate 0)
        to avoid confusion, we automatically add a dummy node.
    """
    def __init__(self):
        self.nodes = [LNODE("dummy", "")]  # type: list[LNODE]
        self.var_count = 0
        self.unused_vars = set()  # variables that are not used, but are present in this context

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
        for index, node in self:
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

    def __len__(self):
        return len(self.nodes)-1


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
