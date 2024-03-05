from collections import defaultdict
from core.cnf import CNF


def determine_tseitin_from_cnf(cnf: CNF) -> set:
    """
    Determine potential tseitin variables.
        We look for patterns of iff clauses head_lit <=> body_literals, and assume head_lit
        is a tseitin variable, unless it also occurs in any of the remaining non iff clauses.
    :param cnf: The CNF to check for tseitin variables.
    :return: a set of tseitin variables
    """
    tseitin_vars = set()
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

    # fake_tseitin_vars contains vars occuring within MULTIPLE tseitin-iffs.
    # these can not be tseitin variables and must be removed from tseitin_vars
    # before returning the result.
    fake_tseitin_vars = set()
    for clause in clauses:
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
                # assert abs(main_lit) not in tseitin_vars, f"Found {main_lit} twice!"
                # history: assert was triggered by var occurring within multiple tseitin iff.
                # we decided to remove these from tseitin_vars before returning it as result.
                if abs(main_lit) in tseitin_vars:
                    fake_tseitin_vars.add(abs(main_lit))
                tseitin_vars.add(abs(main_lit))
    tseitin_vars.difference_update(fake_tseitin_vars)
    return tseitin_vars


# def recover_formula_from_cnf(cnf: CNF) -> VariableSetInfo:
#     """
#     #TODO
#     Determine potential tseitin variables.
#     :param cnf: The CNF to check for tseitin variables.
#     :return: tseitin variables as part of a VariableSetInfo
#     """
#     # separate binary clauses from others for easy contains check later
#     bin_clauses = defaultdict(lambda: set())
#     clauses = list()
#     for clause in cnf.clauses:
#         if len(clause) == 2:
#             lit1 = clause[0]
#             lit2 = clause[1]
#             bin_clauses[lit1].add(lit2)
#             bin_clauses[lit2].add(lit1)
#         else:
#             clauses.append(clause)
#     # detect iff rules
#     iff_clauses = []
#     index = 0
#     while index < len(clauses):
#         clause = clauses[index]
#         if len(clause) > 2:
#             # check whether clause is iff
#             # - determine if any lit in clause is in binary relation with all others
#             main_lit = None
#             for lit in clause:
#                 is_main_lit = all((-lit in bin_clauses[-lit2]) for lit2 in clause if lit != lit2)
#                 if is_main_lit and main_lit is not None:
#                     # If there is more than one main literal, then probably
#                     # this is a mutual exclusivity constraint rather than a
#                     # tseitin originating iff.
#                     main_lit = None
#                     break
#                 main_lit = lit if is_main_lit else main_lit
#             if main_lit is not None:
#                 iff_clauses.append((-main_lit, [l for l in clause if l != main_lit]))
#                 clauses.pop(index)
#                 index -= 1  # next time check same index again
#         index += 1
#
#     # results
#     lf = [None] * (cnf.var_count+1)
#     for (head, body) in iff_clauses:
#         # head <=> body
#         # the body is a disjunction !
#         assert lf[abs(head)] is None
#         if head > 0:
#             lf[head] = (head, "conj", [-x for x in body])
#         else:
#             lf[-head] = (-head, "disj", body)
#
#     # collect potential tseitin variables
#     tseitin_vars = set()
#     for node in lf:
#         if node is not None:
#             index, node_type, body = node
#             tseitin_vars.add(index)
#
#     # remove variables that also occur within remaining clauses.
#     # these can not be tseitin!
#     # TODO: 2024/01/21, WHY NOT?? Their use should be in other clauses, what else is the point, no?
#     # for clause in clauses:
#     #     tseitin_vars.difference_update((abs(x) for x in clause))
#
#     varinfo = VariableSetInfo(node2dict=None, tseitin_vars=tseitin_vars)
#     return varinfo
