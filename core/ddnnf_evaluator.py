from core.ddnnf import DDNNF


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
