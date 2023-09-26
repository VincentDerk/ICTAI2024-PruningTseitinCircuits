import pickle
from collections import defaultdict

from core.cnf2ddnnf import cnf_to_ddnnf
from core.varinfo import VariableSetInfo
from core.cnf import CNF


def compile_wmc_instance(filename_cnf: str, filename_output: str, nnf=False):
    cnf = read_cnf(filename_cnf)
    var_info = determine_tseitin_from_cnf(cnf)

    assert len(var_info.tseitin_vars) > 0,  "No tseitin variables detected."  # could be true, but then no point writing file.

    output_filename_vars = filename_output + "_varinfo.pickle"
    with open(output_filename_vars, "wb") as f:
        pickle.dump(var_info, f)

    # KC
    if nnf:
        ddnnf = cnf_to_ddnnf(cnf)
        # save files
        output_filename_ddnnf = filename_output + "_ddnnf.pickle"
        with open(output_filename_ddnnf, "wb") as f:
            pickle.dump(ddnnf, f)


def read_cnf(filename_cnf: str) -> CNF:
    cnf = CNF()
    with open(filename_cnf, "r") as f:
        for line in f:
            if line.startswith("c"):
                continue
            elif line.startswith("p cnf"):
                varcount = int(line.split(" ")[2])
                cnf.set_atom_count(varcount)
            else:
                line = line.split(" ")
                cnf.add_clause((int(x) for x in line[:-1]))
    return cnf


def determine_tseitin_from_cnf(cnf: CNF) -> VariableSetInfo:
    """
    Determine potential tseitin varibales.
        We look for patterns of iff clauses head_lit <=> body_literals, and assume head_lit
        is a tseitin variable, unless it also occurs in any of the remaining non iff clauses.
    :param cnf: The CNF to check for tseitin variables.
    :return: tseitin variables as part of a VariableSetInfo
    """
    # separate binary clauses from others for easy contains check later
    bin_clauses = defaultdict(lambda: set())
    clauses = list()
    for clause in cnf.clauses:
        if len(clause) == 2:
            lit1 = clause[0]
            lit2 = clause[1]
            bin_clauses[lit1].add(lit2)
            bin_clauses[lit2].add(lit1)
        else:
            clauses.append(clause)
    # detect iff rules
    iff_clauses = []
    index = 0
    while index < len(clauses):
        clause = clauses[index]
        if len(clause) > 2:
            # check whether clause is iff
            # - determine if any lit in clause is in binary relation with all others
            main_lit = None
            for lit in clause:
                is_main_lit = all((-lit in bin_clauses[-lit2]) for lit2 in clause if lit != lit2)
                if is_main_lit and main_lit is not None:
                    # If there is more than one main literal, then probably
                    # this is a mutual exclusivity constraint rather than a
                    # tseitin originating iff.
                    main_lit = None
                    break
                main_lit = lit if is_main_lit else main_lit
            if main_lit is not None:
                iff_clauses.append((-main_lit, [l for l in clause if l != main_lit]))
                clauses.pop(index)
                index -= 1  # next time check same index again
        index += 1

    # results
    lf = [None] * (cnf.var_count+1)
    for (head, body) in iff_clauses:
        # head <=> body
        # the body is a disjunction !
        assert lf[abs(head)] is None
        if head > 0:
            lf[head] = (head, "disj", body)
        else:
            lf[-head] = (-head, "conj", [-x for x in body])

    # collect potential tseitin variables
    tseitin_vars = set()
    for node in lf:
        if node is not None:
            index, node_type, body = node
            tseitin_vars.add(index)

    # remove variables that also occur within remaining clauses.
    # these can not be tseitin!
    for clause in clauses:
        tseitin_vars.difference_update((abs(x) for x in clause))

    varinfo = VariableSetInfo(node2dict=None, tseitin_vars=tseitin_vars)
    return varinfo


if __name__ == "__main__":
    import argparse
    argparser = argparse.ArgumentParser()
    argparser.add_argument("filename_cnf")
    argparser.add_argument("filename_output")
    argparser.add_argument("--nnf", action="store_true")
    argparser.set_defaults(nnf=False)
    args = argparser.parse_args()

    compile_wmc_instance(**vars(args))