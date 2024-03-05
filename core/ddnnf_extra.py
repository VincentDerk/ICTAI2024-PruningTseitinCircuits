import functools

from core.ddnnf import DDNNF, FormulaOverlayList
from core.ddnnf_evaluator import DDNNFTraverserBottomUp


def _polarity(idx):
    """ returns -1 if idx < 0, else 1. """
    return -1 if idx < 0 else 1


def smooth_ddnnf(ddnnf: DDNNF) -> DDNNF:
    """
    Create a smooth version of the given d-DNNF.
    This uses a rather standard simple implementation where we create at most 1 smooth node
    per variable. However, if combinations of smooth nodes appear multiple times, this would not
    be optimized. E.g., if we have to smooth for varset (a,b) and elsewhere in the tree as well,
    we will create twice the node AND(a,b).
    :param ddnnf: the d-DNNF to smooth
    :return: a smoothed version of the given d-DNNF.
    """
    new_ddnnf = DDNNF()
    overlay_new_idx = FormulaOverlayList(ddnnf)
    overlay_varsets = FormulaOverlayList(ddnnf)
    traversor = DDNNFTraverserBottomUp(ddnnf)
    smooth_node_idx = dict()  # maps variable to the idx of a smoothing node for that var.
    for node_idx, node in traversor.next_node():
        if node.node_type == "atom":
            new_idx = new_ddnnf.add_atom(node.node_field)
            overlay_new_idx[node_idx] = new_idx
            overlay_varsets[node_idx] = {node_idx}
        elif node.node_type == "disj":
            # each child must have the same variable set.
            # - compute varset for this node.
            children = node.node_field
            curr_varset = functools.reduce(lambda x, y: x.union(y), (overlay_varsets[abs(idx)] for idx in children))
            # -  for each child, smooth.
            for idx, child_idx in enumerate(children):
                difference_varset = curr_varset.difference(overlay_varsets[abs(child_idx)])
                if len(difference_varset) == 0:
                    children[idx] = _polarity(child_idx) * overlay_new_idx[abs(child_idx)]
                else:
                    # make sure each required smooth node exists.
                    for v in difference_varset:
                        if v not in smooth_node_idx:
                            smooth_idx = new_ddnnf.add_disj((v, -v))
                            smooth_node_idx[v] = smooth_idx
                    # add the smoothing AND node
                    smooth_nodes = tuple((smooth_node_idx[v] for v in difference_varset))
                    and_node_children = (_polarity(child_idx) * overlay_new_idx[abs(child_idx)],) + smooth_nodes
                    new_idx = new_ddnnf.add_conj(and_node_children)
                    children[idx] = new_idx
            # create new OR node.
            new_idx = new_ddnnf.add_disj(children)
            overlay_new_idx[node_idx] = new_idx
            overlay_varsets[node_idx] = curr_varset

        elif node.node_type == "conj":
            children = node.node_field
            new_children = tuple((_polarity(idx) * overlay_new_idx[abs(idx)] for idx in children))
            new_idx = new_ddnnf.add_conj(new_children)
            overlay_new_idx[node_idx] = new_idx
            overlay_varsets[node_idx] = functools.reduce(lambda x, y: x.union(y), (overlay_varsets[abs(idx)] for idx in children))
    return new_ddnnf


def existential_quantification(ddnnf, propagate_vars: set) -> DDNNF:
    """
    Existentially quantify the given variables from the given d-DNNF:
    - the given vars and their negation are replaced by "True", which is
    propagated upwards. Irrelevant nodes are then removed using a simple approach.
    That is, "True or  1" becomes "True", and "True and 1" becomes "1",
    but a Tseitin artifact is not completely removed.

    The given ddnnf is unaffected.

    :param ddnnf: The d-DNNF to existentially quantify
    :param propagate_vars: The variables to existentially quantify.
    :return: A new d-DNNF, from existentially quantifying the given variables on ddnnf.
    """
    # replace propagate_vars with True, and propagate them upwards.
    # overlay_new_idx stores the new node's index (or True if the node is to be removed).
    new_ddnnf = DDNNF()
    overlay_new_idx = FormulaOverlayList(ddnnf)
    traversor = DDNNFTraverserBottomUp(ddnnf)

    for node_idx, node in traversor.next_node():
        if node.node_type == "atom":
            if node_idx in propagate_vars:
                overlay_new_idx[node_idx] = True
            else:
                new_idx = new_ddnnf.add_atom(node.node_field)
                overlay_new_idx[node_idx] = new_idx

        elif node.node_type == "disj":
            children = node.node_field
            child_results = (overlay_new_idx[abs(idx)] is True for idx in children)
            contains_true = any(child_results)
            if contains_true:
                overlay_new_idx[node_idx] = True
            else:
                new_children = tuple(
                    (_polarity(idx) * overlay_new_idx[abs(idx)] for idx in children))
                new_idx = new_ddnnf.add_disj(new_children)
                overlay_new_idx[node_idx] = new_idx

        elif node.node_type == "conj":
            children = node.node_field
            new_children = [_polarity(idx) * overlay_new_idx[abs(idx)] for idx in children if
                            overlay_new_idx[abs(idx)] is not True]
            if len(new_children) == 0:
                overlay_new_idx[node_idx] = True
            elif len(new_children) == 1:
                child_idx = new_children[0]
                overlay_new_idx[node_idx] = _polarity(child_idx) * overlay_new_idx[abs(child_idx)]
            else:
                new_idx = new_ddnnf.add_conj(new_children)
                overlay_new_idx[node_idx] = new_idx
    return new_ddnnf


def ddnnf_to_dot(ddnnf, prop_function=None) -> str:
    """Write out in GraphViz (dot) format.
    :param prop_function: a property function. Given a tuple of index, node (of the ddnnf),
        it should return a string containing additional properties for the node.
        By default, the empty string is currently returned.
    :param ddnnf: to create dot representation of
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
