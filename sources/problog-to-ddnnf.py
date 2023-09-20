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
import subprocess
import sys
import tempfile
import time
import os
from collections import defaultdict
from typing import Tuple, List, Dict

from problog.ddnnf_formula import DSharpError
from problog.formula import LogicDAG
from problog.program import PrologFile
from problog.logic import Term
from problog.engine import DefaultEngine

from core.cnf import CNF
from core.ddnnf import DDNNF, FormulaOverlayList
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
                if node.name is None or node.name.functor.startswith("body_"):
                    tseitin_vars.append(index)
            elif nodetype == "disj":
                cnf.add_iff_disj(index, *node.children)
                if node.name is None or node.name.functor.startswith("body_"):
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


def cnf_to_ddnnf(cnf: CNF, k="dsharp"):
    return _compile_with_dsharp(cnf, smooth=True)

def _compile_with_dsharp(cnf, smooth=True):
    result = None
    with Timer("DSharp compilation"):
        fd1, cnf_file = tempfile.mkstemp(".cnf")
        fd2, nnf_file = tempfile.mkstemp(".nnf")
        os.close(fd1)
        os.close(fd2)
        if smooth:
            smoothl = ["-smoothNNF"]
        else:
            smoothl = []
        cmd = ["./bin/dsharp", "-Fnnf", nnf_file] + smoothl + ["-disableAllLits", cnf_file]  #

        try:
            result = _compile(cnf, cmd, cnf_file, nnf_file)
        except subprocess.CalledProcessError:
            raise DSharpError()

        try:
            os.remove(cnf_file)
        except OSError:
            pass
        try:
            os.remove(nnf_file)
        except OSError:
            pass

    return result


def _compile(cnf, cmd, cnf_file, nnf_file):
    assert cnf.clause_count() > 0
    with open(cnf_file, "w") as f:
        f.write(cnf.to_dimacs())

    try:
        result = subprocess.run(cmd, shell=False, check=True, stdout=subprocess.DEVNULL)
        success = result.returncode == 0
        if not success:
            raise DSharpError()
    except subprocess.CalledProcessError as err:
        print(err)
        raise err
    return _load_nnf(nnf_file)


def _load_nnf(filename):
    nnf = DDNNF()

    with open(filename) as f:
        num_literal_nodes = 0

        # Create map: each literal l with line nr X to index l
        line2idx = {}
        for line_nr0, line in enumerate(f):
            line_nr = line_nr0  # +0, bc "nnf" is a line (-1), and we count from 1 (+1)
            # print(line)
            line = line.strip().split()
            if line[0] == "L":
                l = int(line[1])
                # I assume each literal is from 1..N.
                assert l <= num_literal_nodes, f"l was {l}. num_lit_nodes is {num_literal_nodes}"
                # what used to be at line_nr, is now at index l
                line2idx[line_nr] = l
            elif line[0] == "nnf":
                num_literal_nodes = int(line[3])

        # Create atoms
        assert len(line2idx) == num_literal_nodes * 2
        for l in range(1, num_literal_nodes+1):
            nnf.add_atom(node_field=l)  # field is irrelevant for now.

        f.seek(0)  # reset file position so we can iterate over it again
        # Add conj and disjunction nodes
        # correctly remapping each line reference
        conj_cache = dict()  # cache so we do not create duplicate nodes.
        disj_cache = dict()  # added because dsharp creates multiple smooth nodes.
        for line_nr0, line in enumerate(f):
            line_nr = line_nr0  # +0, bc "nnf" is a line (-1), and we count from 1 (+1)
            line = line.strip().split()
            if line[0] == "A":
                # line[1] = number of children (ignore)
                # line[2:] = all children
                children = tuple(line2idx[int(l)+1] for l in line[2:])
                cache_value = conj_cache.get(children, None)
                if cache_value is None:
                    node_idx = nnf.add_conj(children)
                    conj_cache[children] = node_idx
                else:
                    node_idx = cache_value
                line2idx[line_nr] = node_idx
            elif line[0] == "O":
                # line[1] = decision on which basis the children differ
                # line[2] = number of children
                # line[3:] = all children
                children = tuple(line2idx[int(l)+1] for l in line[3:])
                cache_value = disj_cache.get(children, None)
                if cache_value is None:
                    node_idx = nnf.add_disj(children)
                    disj_cache[children] = node_idx
                else:
                    node_idx = cache_value
                line2idx[line_nr] = node_idx
    return nnf



if __name__ == "__main__":
    import argparse
    argparser = argparse.ArgumentParser()
    argparser.add_argument("filename")
    argparser.add_argument("output_filename")
    args = argparser.parse_args()

    main(**vars(args))
