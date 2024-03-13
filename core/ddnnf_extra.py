import functools

from graphviz import Source

from core.ddnnf import DDNNF, FormulaOverlayList
from core.ddnnf_evaluator import DDNNFTraverserBottomUp, DDNNFTraverserTopDown
from detafter.postdetector import get_tseitin_artifacts


def get_overlay_variables(ddnnf, ignore_vars=None) -> FormulaOverlayList:
    """
    Create an overlay of the variables used within each node.
    :param ddnnf: The d-DNNF to create an overlay for.
    :param ignore_vars: The variables to ignore. Ideally contains is a fast method.
    :return: An overlay for ddnnf where each node has its set of variables stored.
    """
    if ignore_vars is None:
        ignore_vars = set()
    overlay_varsets = FormulaOverlayList(ddnnf)
    traversor = DDNNFTraverserBottomUp(ddnnf)
    for node_idx, node in traversor.next_node():
        if node.node_type == "atom":
            overlay_varsets[node_idx] = {node_idx} if node_idx not in ignore_vars else set()
        elif node.node_type == "disj" or node.node_type == "conj":
            children = node.node_field
            overlay_varsets[node_idx] = functools.reduce(lambda x, y: x.union(y),
                                                         (overlay_varsets[abs(idx)] for idx in
                                                          children))
    return overlay_varsets


def active_nodes_overlay(ddnnf: DDNNF) -> FormulaOverlayList:
    """
    Create an overlay, capturing the active nodes of each node.
    A node is active if it is connected to the root (final) node of ddnnf.
    :param ddnnf: The d-DNNF to create an overlay for.
    :return: An overlay for ddnnf where each active node is True, the others False.
    """
    overlay_active = FormulaOverlayList(ddnnf)
    traversor = DDNNFTraverserTopDown(ddnnf)
    overlay_active[-1] = True
    for node_idx, node in traversor.next_node():
        # if current node is active, activate children
        if overlay_active[node_idx] is True:
            if node.node_type == "disj" or node.node_type == "conj":
                children = node.node_field
                for child_idx in children:
                    overlay_active[abs(child_idx)] = True
        else:
            assert overlay_active[abs(node_idx)] is None
            overlay_active[abs(node_idx)] = False
    return overlay_active


def get_overlay_parent_count(ddnnf: DDNNF) -> FormulaOverlayList:
    """
    Create an overlay, storing the number of parents for each node.
    :param ddnnf: The d-DNNF to create an overlay for.
    :return: An overlay for ddnnf where each node has its number of parent nodes stored.
    """
    overlay_parents = FormulaOverlayList(ddnnf)
    traversor = DDNNFTraverserBottomUp(ddnnf)
    for node_idx, node in traversor.next_node():
        overlay_parents[node_idx] = 0
        if node.node_type == "disj" or node.node_type == "conj":
            children = node.node_field
            for child_idx in children:
                overlay_parents[abs(child_idx)] += 1
    return overlay_parents


def _polarity(idx):
    """ returns -1 if idx < 0, else 1. """
    return -1 if idx < 0 else 1


#
# ----------
#

def existential_quantification_tseitin(ddnnf, tseitin_vars: set) -> DDNNF:
    new_ddnnf = DDNNF()
    new_ddnnf.unused_vars.update(ddnnf.unused_vars.difference(tseitin_vars))
    overlay_artifact = get_tseitin_artifacts(ddnnf, tseitin_vars)

    # mark nodes for removal - top/down
    traversor = DDNNFTraverserTopDown(ddnnf)
    overlay_active = FormulaOverlayList(ddnnf)
    overlay_active[-1] = True
    for node_idx, node in traversor.next_node():
        # we set each child to active, unless they are an artifact.
        # if we encounter a node that is not active -> it has no active parent.
        if overlay_active[node_idx]:
            if node.node_type == "disj" or node.node_type == "conj":
                children = node.node_field
                for child_idx in children:
                    overlay_active[abs(child_idx)] = not overlay_artifact[abs(child_idx)]
        else:
            overlay_active[node_idx] = False
    # del overlay_artifact  # not needed anymore, use overlay_active

    # create new-ddnnf bottom up
    overlay_new_idx = FormulaOverlayList(ddnnf)
    traversor = DDNNFTraverserBottomUp(ddnnf)
    for node_idx, node in traversor.next_node():
        if node.node_type == "atom":
            if overlay_active[node_idx]:
                new_idx = new_ddnnf.add_atom(node.node_field)
                overlay_new_idx[node_idx] = new_idx
            else:
                # def _prop_function(i, _node):
                #     if _node.node_type == "atom" and not overlay_active[i]:
                #         return 'fillcolor="blue"'
                #     elif overlay_artifact[i]:
                #         return f'label="{i}", fillcolor="green"'
                #     elif _node.node_type == "atom" and _node.node_field in tseitin_vars:
                #         return 'fillcolor="yellow"'
                #     elif not overlay_active[i]:
                #         return f'label="{i}", fillcolor="red"'
                #     else:
                #         return 'fillcolor="white"'
                # Source(ddnnf_to_dot(ddnnf, _prop_function)).render(view=True)
                new_ddnnf.unused_vars.add(node.node_field)
        elif node.node_type == "disj":
            if overlay_active[node_idx]:
                children = node.node_field
                # if a disj is not an artifact, then its direct children are not either.
                # by definition of d-DNNF, artifact, and model counts.
                assert all(overlay_active[abs(idx)] for idx in children)
                new_children = tuple((_polarity(idx) * overlay_new_idx[abs(idx)] for idx in children))
                new_idx = new_ddnnf.add_disj(new_children)
                overlay_new_idx[node_idx] = new_idx
        elif node.node_type == "conj":
            if overlay_active[node_idx]:
                children = node.node_field
                new_children = tuple((_polarity(idx) * overlay_new_idx[abs(idx)] for idx in children if overlay_active[abs(idx)]))
                if len(new_children) == 1:
                    overlay_new_idx[node_idx] = new_children[0]
                else:
                    assert len(new_children) > 1, ("== 0 is impossible because if each child is "
                                                   "an artifact, then this node can not be active.")
                    new_idx = new_ddnnf.add_conj(new_children)
                    overlay_new_idx[node_idx] = new_idx
    # we only removed artifacts.
    # now existentially quantify all tseitin variables not in an artifact.
    new_ddnnf = existential_quantification(new_ddnnf, tseitin_vars)
    return new_ddnnf


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
    new_ddnnf.unused_vars.update(ddnnf.unused_vars)
    overlay_new_idx = FormulaOverlayList(ddnnf)
    overlay_varsets = FormulaOverlayList(ddnnf)
    # overlay_parent_count --
    # to reduce memory, we track for each node the number of yet to compute parents.
    # if it becomes 0, we can remove varset for that node.
    overlay_parent_count = get_overlay_parent_count(ddnnf)  # reduces number of stored sets in overlay_varsets
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
            new_children = list(children)
            curr_varset = functools.reduce(lambda x, y: x.union(y), (overlay_varsets[abs(idx)] for idx in children))
            # -  for each child, smooth.
            for idx, child_idx in enumerate(children):
                difference_varset = curr_varset.difference(overlay_varsets[abs(child_idx)])
                if len(difference_varset) == 0:
                    new_children[idx] = _polarity(child_idx) * overlay_new_idx[abs(child_idx)]
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
                    new_children[idx] = new_idx
            # create new OR node.
            new_idx = new_ddnnf.add_disj(tuple(new_children))
            overlay_new_idx[node_idx] = new_idx
            overlay_varsets[node_idx] = curr_varset

            # reduce memory -- update unused parent count for children
            # if count becomes 0; clear overlay_varsets for that child.
            for child_idx in children:
                overlay_parent_count[abs(child_idx)] -= 1
                if overlay_parent_count[abs(child_idx)] == 0:
                    overlay_varsets[abs(child_idx)] = None

        elif node.node_type == "conj":
            children = node.node_field
            new_children = tuple((_polarity(idx) * overlay_new_idx[abs(idx)] for idx in children))
            new_idx = new_ddnnf.add_conj(new_children)
            overlay_new_idx[node_idx] = new_idx
            overlay_varsets[node_idx] = functools.reduce(lambda x, y: x.union(y), (overlay_varsets[abs(idx)] for idx in children))

            # reduce memory -- update unused parent count for children
            # if count becomes 0; clear overlay_varsets for that child.
            for child_idx in children:
                overlay_parent_count[abs(child_idx)] -= 1
                if overlay_parent_count[abs(child_idx)] == 0:
                    overlay_varsets[abs(child_idx)] = None
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
    new_ddnnf.unused_vars.update(ddnnf.unused_vars.difference(propagate_vars))
    overlay_new_idx = FormulaOverlayList(ddnnf)
    traversor = DDNNFTraverserBottomUp(ddnnf)

    for node_idx, node in traversor.next_node():
        if node.node_type == "atom":
            if node.node_field in propagate_vars:
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
                overlay_new_idx[node_idx] = new_children[0]
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


#
#
# ----- Overlays methods -----
#
#


def compress_ddnnf(ddnnf: DDNNF) -> DDNNF:
    """
    Compresses the given d-DNNF.
    - Remove nodes not contributing (connected) to the root node. If an atom is not used,
    it is moved to the unused_vars set.

    In the future, more optimisations may be included.
    :param ddnnf: the d-DNNF to compress.
    :return: A new, compressed, d-DNNF object.
    """
    overlay_active = active_nodes_overlay(ddnnf)
    overlay_new_idx = FormulaOverlayList(ddnnf)
    new_ddnnf = DDNNF()
    new_ddnnf.unused_vars = ddnnf.unused_vars.copy()
    traversor = DDNNFTraverserBottomUp(ddnnf)
    for node_idx, node in traversor.next_node():
        if overlay_active[node_idx]:
            if node.node_type == "atom":
                new_idx = new_ddnnf.add_atom(node.node_field)
            elif node.node_type == "disj":
                new_children = tuple((_polarity(idx) * overlay_new_idx[abs(idx)] for idx in node.node_field))
                new_idx = new_ddnnf.add_disj(new_children)
            else:
                assert node.node_type == "conj"
                new_children = tuple((_polarity(idx) * overlay_new_idx[abs(idx)] for idx in node.node_field))
                new_idx = new_ddnnf.add_conj(new_children)
            overlay_new_idx[node_idx] = new_idx
        else:
            if node.node_type == "atom":
                new_ddnnf.unused_vars.add(node.node_field)
    return new_ddnnf




