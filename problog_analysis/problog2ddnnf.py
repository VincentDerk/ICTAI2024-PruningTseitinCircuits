from problog.formula import LogicDAG
from problog.program import PrologFile
from problog.engine import DefaultEngine

from core.cnf import CNF
from core.cnf2ddnnf import cnf_to_ddnnf
from core.ddnnf import DDNNF
from core.varinfo import VariableSetInfo


def problog_file_to_ddnnf(filename, timeout):
    model = PrologFile(filename)
    return problog_model_to_ddnnf(model, timeout)


def problog_model_to_ddnnf(model, timeout) -> (DDNNF, int, VariableSetInfo):
    """
    :param model: ProbLog model containing one query, and no evidence.
    :param timeout:
    Relevant exceptions are subprocess.CalledProcessError, subprocess.TimeoutExpired, MemoryError
    :return: The DDNNF, compilation time, and Variable info.
    """
    engine = DefaultEngine(label_all=True)
    db = engine.prepare(model)
#    queries = engine.query(db, Term("query", None))
#    evidence = engine.query(db, Term("evidence", None, None))
#    print("Queries:", ", ".join([str(q[0]) for q in queries]))
#    print("Evidence:", ", ".join(["%s=%s" % ev for ev in evidence]))
    gp = engine.ground_all(db)
    # print_lf_compact(gp)
    gp = LogicDAG.createFrom(gp)
    # print_lf_compact(gp)
    cnf, var_info = logicdag_to_cnf(gp)
#    print_cnf(cnf)
#    print(var_info)
    ddnnf, compile_time = cnf_to_ddnnf(cnf, timeout=timeout)
    return ddnnf, compile_time, var_info


def logicdag_to_cnf(dag: LogicDAG) -> (CNF, VariableSetInfo):
    """Transform an acyclic propositional program to a CNF using Clark's completion.

    :param dag: acyclic program to transform
    :return: the cnf, tseitin introduced variables
    """
    cnf = CNF()
    tseitin_vars = list()
    node2name = dict()
    # Each rule in the source formula will correspond to an atom.
    num_atoms = len(dag)

    # Add atoms.
    cnf.set_atom_count(num_atoms)

    # Complete other nodes
    # Note: assumes negation is encoded as negative number.
    # Note: index starts counting from 1
    for index, node, nodetype in dag:
        if node.name is not None:
            node2name[index] = str(node.name)
        if nodetype == "conj":
            cnf.add_iff_conj(index, *node.children)
            #if node.name is None or node.name.functor.startswith(
            #        "body_") or node.name.functor.startswith("problog_cv_"):
            tseitin_vars.append(index)
        elif nodetype == "disj":
            cnf.add_iff_disj(index, *node.children)
            #if node.name is None or node.name.functor.startswith(
            #        "body_") or node.name.functor.startswith("problog_cv_"):
            tseitin_vars.append(index)
        elif nodetype == "atom":
            pass
        else:
            raise ValueError("Unexpected node type: '%s'" % nodetype)

    # Copy constraints.
    for c in dag.constraints():
        for clause in c.as_clauses():
            cnf.add_clause(clause)

    # add query as constraint
    query_node = [node_idx for (query_name, node_idx) in dag.queries()]
    assert len(query_node) == 1
    query_node = query_node[0]
    cnf.add_clause([query_node])

    # remove query from Tseitin vars
    tseitin_vars.remove(query_node)
    return cnf, VariableSetInfo(node2name, tseitin_vars)

