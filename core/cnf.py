
class CNF:
    """

    Assumptions:
        * Variables are 1-n. (0 is reserved)
        * Literals are variables l or their negation (-l)
        * Each variable is used in at least one clause
    """

    def __init__(self):
        self.var_count = 0
        self.clauses = list()

    # ------------- #
    # --- ATOMS --- #
    # ------------- #
    def add_atom(self):
        self.var_count += 1

    def set_atom_count(self, atomcount):
        self.var_count = atomcount

    # ------------- #
    # -- CLAUSES -- #
    # ------------- #
    def clause_count(self):
        return len(self.clauses)

    def add_clause(self, literals):
        self.clauses.append(list(literals))

    def add_iff_disj(self, head: int, *body):
        """ Add clause of the form head <=> b1 or b2 or b3 or ..."""
        assert isinstance(head, int)
        # head => body
        clause = list(body)
        clause.append(-head)
        self.clauses.append(clause)
        # body => head
        # b1 v b2 => h
        # (~b1 & ~b2) v h
        # h v ~b1
        # h v ~b2
        for lit in body:
            self.clauses.append([head, -lit])

    def add_iff_conj(self, head: int, *body):
        """ Add clause of the form head <=> b1 and b2 and b3 and ..."""
        assert isinstance(head, int)
        # body => head
        # ~b1 or ~b2 or ... or head
        clause = list(-x for x in body)
        clause.append(head)
        self.clauses.append(clause)
        # head => body
        # ~h or (b1 and b2 and ...)
        # ~h or b1
        # ~h or b2
        for lit in body:
            self.clauses.append([-head, lit])

    def to_dimacs(self):
        """Transform to a string in DIMACS format.
        :return: string in DIMACS format
        """
        t = "cnf"
        result = f"p cnf {self.var_count} {self.clause_count()}\n"

        def _clause_to_str(cl):
            return " ".join((str(l) for l in cl)) + " 0"
        result += "\n".join((map(_clause_to_str, self.clauses)))
        return result


def read_cnf(filename_cnf: str) -> CNF:
    """ read CNF from DIMACS file. """
    cnf = CNF()
    with open(filename_cnf, "r") as f:
        for line in f:
            if line.startswith("c"):
                continue
            elif line.startswith("p cnf"):
                varcount = int(line.split(" ")[2])
                cnf.set_atom_count(varcount)
            else:
                line2 = line.replace("  ", " ").strip().split(" ")
                if len(line2) > 1:  # if line only contains enter, do nothing.
                    cnf.add_clause((int(x) for x in line2[:-1]))
    return cnf
