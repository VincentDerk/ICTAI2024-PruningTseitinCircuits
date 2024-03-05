from core.ddnnf import DDNNF


class DDNNFTraverserBottomUp:

    def __init__(self, ddnnf: DDNNF):
        self.ddnnf = ddnnf

    def next_node(self):
        """ Bottom up evaluation of each node.

        Since a d-DNNF is stored such that the children precede the parents,
            we can simply go over the list from index 0 to index N.
        """
        for index, node in self.ddnnf:
            yield index, node


class DDNNFTraverserTopDown:

    def __init__(self, ddnnf: DDNNF):
        self.ddnnf = ddnnf

    def next_node(self):
        """ Top down evaluation of each node.

        Since a d-DNNF is stored such that the children precede the parents,
            we can simply go over the list from index N to index 1. (index 0 is the dummy)
        """
        nb_nodes = len(self.ddnnf)
        for index in range(nb_nodes, 0, -1):
            yield index, self.ddnnf[index]


def compute_model_count(ddnnf: DDNNF) -> int:
    variables = [None] * (len(ddnnf)+1)
    mc = [None] * (len(ddnnf)+1)
    for node_index, node in ddnnf:
        if node.node_type == "atom":
            variables[node_index] = {node_index}
            mc[node_index] = 1
        elif node.node_type == "conj":
            children = node.node_field
            variables[node_index] = set()
            for child in children:
                child_vars = variables[abs(child)]
                variables[node_index].update(child_vars)
            mc[node_index] = 1
            for child in children:
                mc[node_index] *= mc[abs(child)]
        else:
            assert node.node_type == "disj"
            children = node.node_field
            variables[node_index] = set()
            for child in children:
                child_vars = variables[abs(child)]
                variables[node_index].update(child_vars)
            total_nb_vars = len(variables[node_index])
            mc[node_index] = 0
            for child in children:
                mc[node_index] += mc[abs(child)] * 2**(total_nb_vars - len(variables[abs(child)]))
    return mc[-1]


