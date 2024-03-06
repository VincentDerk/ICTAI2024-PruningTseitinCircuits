import functools
from typing import Collection, Set, Tuple

from core.ddnnf import DDNNF, FormulaOverlayList
from core.ddnnf_evaluator import DDNNFTraverserBottomUp


def get_tseitin_artifacts(ddnnf: DDNNF, tseitin_vars: Collection[int]) -> FormulaOverlayList:
    """
    Get an overlay indicating for each node whether it is a tseitin artifact.
    A node is a tseitin artifact iff the model count of that node is equal to 2**n with
        n the number of non-tseitin variables. Such nodes can be replaced by a node smoothing over
        all n non-tseitin variables.
    :param ddnnf: The d-DNNF to search the artifacts in.
    :param tseitin_vars: The tseitin variables. Ideally this has a fast contains method.
    :return: A d-DNNF formula overlay denoting for each node whether it is a tseitin artifact.
    """
    overlay_mc = FormulaOverlayList(ddnnf)  # unweighted model count (incl. smoothing) of each node
    overlay_varset = FormulaOverlayList(ddnnf)  # set of non-tseitin variables in each node
    overlay_artifact = FormulaOverlayList(ddnnf)  # whether node is a tseitin artifact

    traversor = DDNNFTraverserBottomUp(ddnnf)
    for node_idx, node in traversor.next_node():
        if node.node_type == "atom":
            overlay_mc[node_idx] = 1
            overlay_varset[node_idx] = {node.node_field} if node.node_field not in tseitin_vars else set()
            overlay_artifact[node_idx] = False
        elif node.node_type == "disj":
            children = node.node_field
            node_varset = functools.reduce(lambda x, y: x.union(y), (overlay_varset[abs(idx)] for idx in children))
            varset_size = len(node_varset)
            node_mc = 0
            for idx in children:
                node_mc += overlay_mc[abs(idx)] * 2**(varset_size - len(overlay_varset[abs(idx)]))
            overlay_mc[node_idx] = node_mc
            overlay_varset[node_idx] = node_varset
            overlay_artifact[node_idx] = node_mc == 2**varset_size
        elif node.node_type == "conj":
            children = node.node_field
            overlay_mc[node_idx] = functools.reduce(lambda x, y: x * y, (overlay_mc[abs(idx)] for idx in children))
            overlay_varset[node_idx] = functools.reduce(lambda x, y: x.union(y), (overlay_varset[abs(idx)] for idx in children))
            overlay_artifact[node_idx] = overlay_mc[node_idx] == 2**len(overlay_varset[node_idx])
    return overlay_artifact



# def get_tseitin_artifacts(ddnnf: DDNNF, tseitin_vars: Collection[int]) -> FormulaOverlayList:
#     """
#     Get a list of tseitin artifacts within the given d-DNNF.
#
#     A node is a tseitin artifact iff the model count of that node is equal to 2**n with
#         n the number of non-tseitin variables. Such nodes can be replaced by a node smoothing over
#         all n non-tseitin variables.
#     :param ddnnf: The d-DNNF to search the artifacts in.
#     :param tseitin_vars: A collection of tseitin variables. Ideally this has a fast contains method.
#     :return: A d-DNNF formula overlay denoting for each node whether it is a tseitin artifact,
#         and an overlay with the set of variables for each node.
#     """
#     # for each node, determine:
#     # - its unweighted model count (assume smoothing has happened)
#     # - the set of variables involved in the node itself or nodes below it.
#
#     # compute model counts and variable sets (set of non-tseitin vars)
#     overlay_mc = get_overlay_model_count(ddnnf)
#     overlay_contains_tseitin = get_overlay_contains_tseitin(ddnnf, tseitin_vars=tseitin_vars)
#     overlay_varsets = get_overlay_variables(ddnnf, ignore_vars=tseitin_vars)
#
#     # check for each node whether it is an artifact based on model count.
#     overlay_artifact = FormulaOverlayList(ddnnf)
#     traversor = DDNNFTraverserBottomUp(ddnnf)
#     for node_idx, node in traversor.next_node():
#         if node.node_type == "atom":
#             overlay_artifact[node_idx] = False
#         elif node.node_type == "disj":
#             num_non_tseitin_vars = len(overlay_varsets[node_idx])
#             contains_tseitin = overlay_contains_tseitin[node_idx]
#             is_artifact = (overlay_mc[node_idx] == 2 ** num_non_tseitin_vars) and contains_tseitin
#             overlay_artifact[node_idx] = is_artifact
#         elif node.node_type == "conj":
#             children = node.node_field
#             is_artifact = all(overlay_artifact[idx] for idx in children)
#             overlay_artifact[node_idx] = is_artifact
#     return overlay_artifact


# def get_overlay_contains_tseitin(ddnnf, tseitin_vars: Collection[int]) -> FormulaOverlayList:
#     """
#     Create an overlay, capturing for each node whether it contains a tseitin variable.
#     :param ddnnf: The d-DNNF to create an overlay for.
#     :param tseitin_vars: The tseitin variables
#     :return: An overlay for ddnnf indicating for each node whether it contains a tseitin var.
#     """
#     overlay_varsets = FormulaOverlayList(ddnnf)
#     traversor = DDNNFTraverserBottomUp(ddnnf)
#     for node_idx, node in traversor.next_node():
#         if node.node_type == "atom":
#             overlay_varsets[node_idx] = node_idx in tseitin_vars
#         elif node.node_type == "disj":
#             children = node.node_field
#             overlay_varsets[node_idx] = any((overlay_varsets[abs(idx)] for idx in children))
#         elif node.node_type == "conj":
#             children = node.node_field
#             overlay_varsets[node_idx] = any((overlay_varsets[abs(idx)] for idx in children))
#     return overlay_varsets


# def get_overlay_model_count(sddnnf) -> FormulaOverlayList:
#     """
#     Create an overlay, capturing the unweighted model count for each node.
#         This assumes the ddnnf is already smooth, otherwise the result may be incorrect.
#     :param sddnnf: The smooth d-DNNF to create an overlay for.
#     :return: An overlay for ddnnf where each node has its set model count stored.
#     """
#     overlay_mc = FormulaOverlayList(sddnnf)
#     traversor = DDNNFTraverserBottomUp(sddnnf)
#     for node_idx, node in traversor.next_node():
#         if node.node_type == "atom":
#             overlay_mc[node_idx] = 1
#         elif node.node_type == "disj":
#             children = node.node_field
#             overlay_mc[node_idx] = sum((overlay_mc[abs(idx)] for idx in children))
#         elif node.node_type == "conj":
#             children = node.node_field
#             overlay_mc[node_idx] = functools.reduce(lambda x, y: x * y, (overlay_mc[abs(idx)]
#                                                                          for idx in children))
#     return overlay_mc


# def get_overlay_parents(ddnnf) -> FormulaOverlayList:
#     """
#     Create an overlay, capturing the parents of each node.
#     :param ddnnf: The d-DNNF to create an overlay for.
#     :return: An overlay for ddnnf where each node has its set of parent nodes stored.
#     """
#     overlay_parents = FormulaOverlayList(ddnnf, default_constructor=lambda x, y: set())
#     for node_idx, node in ddnnf:
#         if node.node_type == "atom":
#             pass
#         elif node.node_type == "disj" or node.node_type == "conj":
#             children = node.node_field
#             for child_idx in children:
#                 overlay_parents[abs(child_idx)].add(node_idx)
#     return overlay_parents


# def get_artifact_size(ddnnf: DDNNF,
#                       overlay_artifact: FormulaOverlayList,
#                       tseitin_vars: Set[int]) -> Tuple[int, int, int]:
#     """
#
#     :return: The number of nodes fewer, the number of nodes removed, the number of new nodes added
#     """
#     # 1. Check which variables already have a smooth node.
#     smoothed_vars = _vars_smoothed_over(ddnnf)
#
#     # 2. Determine which nodes would be removed
#     # - mark every node below an artifact as prunable
#     overlay_parents = get_overlay_parents(ddnnf)
#     overlay_marked = FormulaOverlayList(ddnnf, default_constructor=lambda x,y: False)
#
#     def _mark_children_dfs(node_idx):
#         if not overlay_marked[node_idx]:
#             deletable = all(overlay_marked[parent_idx] for parent_idx in overlay_parents[node_idx])
#             if deletable:
#                 overlay_marked[node_idx] = True
#                 if ddnnf[node_idx].node_type != "atom":
#                     for child_idx in ddnnf[node_idx].node_field:
#                         _mark_children_dfs(abs(child_idx))
#
#     for index, is_artifact in enumerate(overlay_artifact):
#         if is_artifact:
#             overlay_marked[index] = True
#             # set its children
#             for child_idx in ddnnf[index].node_field:
#                 _mark_children_dfs(abs(child_idx))
#
#     num_deletable = sum(overlay_marked.overlay)
#
#     # 3. Determine across entire circuit, by removing artifact nodes, which variables they covered,
#     # and how many new smooth nodes are required.
#     total_covered_vars = set()
#     overlay_varset = get_overlay_variables(ddnnf, ignore_vars=tseitin_vars)
#     for index, is_artifact in enumerate(overlay_artifact):
#         if is_artifact:
#             total_covered_vars.update(overlay_varset[index])
#     # new_smooth_nodes_for = total_covered_vars.difference(smoothed_vars)
#     num_new_smooth_nodes = len(total_covered_vars.difference(smoothed_vars))
#     # 4. return results
#     num_nodes_less = num_deletable - num_new_smooth_nodes
#     return num_nodes_less, num_deletable, num_new_smooth_nodes


# def _vars_smoothed_over(ddnnf) -> Set[int]:
#     """ all variables in the ddnnf that are smoothed over at least once. """
#     return {abs(node.node_field[0]) for (index, node) in ddnnf if
#             node.node_type == "disj" and
#             len(node.node_field) == 2 and
#             node.node_field[0] == -node.node_field[1]
#             }


