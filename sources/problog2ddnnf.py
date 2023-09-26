#! /usr/bin/env python
"""
Part of the ProbLog distribution.

Copyright 2015 KU Leuven, DTAI Research Group

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import pickle
import time
from typing import Tuple

from problog.formula import LogicDAG
from problog.program import PrologFile
from problog.logic import Term
from problog.engine import DefaultEngine

from core.cnf import CNF
from core.cnf2ddnnf import cnf_to_ddnnf
from core.varinfo import VariableSetInfo


class Timer(object):
    def __init__(self, msg):
        self.message = msg
        self.start_time = None

    def __enter__(self):
        self.start_time = time.time()

    def __exit__(self, *args):
        print("%s: %.4fs" % (self.message, time.time() - self.start_time))


def main(filename, output_filename, k="dsharp"):

    model = PrologFile(filename)
    engine = DefaultEngine(label_all=True)

    with Timer("parsing"):
        db = engine.prepare(model)

    print("\n=== Queries ===")
    queries = engine.query(db, Term("query", None))
    print("Queries:", ", ".join([str(q[0]) for q in queries]))

    print("\n=== Evidence ===")
    evidence = engine.query(db, Term("evidence", None, None))
    print("Evidence:", ", ".join(["%s=%s" % ev for ev in evidence]))

    print("\n=== Ground Program ===")
    with Timer("ground"):
        gp = engine.ground_all(db)
    # print_lf_compact(gp)

    print("\n=== Acyclic Ground Program ===")
    with Timer("acyclic"):
        gp = LogicDAG.createFrom(gp)
    print_lf_compact(gp)

    print("\n=== Conversion to CNF ===")
    cnf, var_info = logicdag_to_cnf(gp)
#    print_cnf(cnf)
    print(var_info)

    print("\n=== Compile to d-DNNF ===")
    with Timer("Knowledge Compilation"):
        ddnnf = cnf_to_ddnnf(cnf)

    # save files
    output_filename_ddnnf = output_filename + "_ddnnf.pickle"
    with open(output_filename_ddnnf, "wb") as f:
        pickle.dump(ddnnf, f)

    output_filename_vars = output_filename + "_varinfo.pickle"
    with open(output_filename_vars, "wb") as f:
        pickle.dump(var_info, f)


def print_lf_compact(lf):
    for index, node, node_type in lf:
        if node_type == "atom":
            print(
                f"{index}: {node_type}\tname={str(node.name).ljust(25)}\tprob={node.probability}"
            )
        elif node_type == "disj" or node_type == "conj":
            print(
                f"{index}: {node_type}\tname={str(node.name).ljust(25)}\tchildren={node.children}"
            )
        else:
            print(f"unsupported node type: {node_type}")


def logicdag_to_cnf(dag: LogicDAG) -> Tuple[CNF, VariableSetInfo]:
    """Transform an acyclic propositional program to a CNF using Clark's completion.

    :param dag: acyclic program to transform
    :return: the cnf, tseitin introduced variables (includes those with starting-name body_)
    """
    with Timer("Clark's completion"):
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
                if node.name is None or node.name.functor.startswith("body_") or node.name.functor.startswith("problog_cv_"):
                    tseitin_vars.append(index)
            elif nodetype == "disj":
                cnf.add_iff_disj(index, *node.children)
                if node.name is None or node.name.functor.startswith("body_") or node.name.functor.startswith("problog_cv_"):
                    tseitin_vars.append(index)
            elif nodetype == "atom":
                pass
            else:
                raise ValueError("Unexpected node type: '%s'" % nodetype)

        # Copy constraints.
        for c in dag.constraints():
            for clause in c.as_clauses():
                cnf.add_clause(clause)

        return cnf, VariableSetInfo(node2name, tseitin_vars)






if __name__ == "__main__":
    import argparse
    argparser = argparse.ArgumentParser()
    argparser.add_argument("filename")
    argparser.add_argument("output_filename")
    args = argparser.parse_args()

    main(**vars(args))
