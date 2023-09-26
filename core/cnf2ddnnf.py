import os
import subprocess
import tempfile

from problog.ddnnf_formula import DSharpError

from core.cnf import CNF
from core.ddnnf import DDNNF


def cnf_to_ddnnf(cnf: CNF, k="dsharp") -> DDNNF:
    return _compile_with_dsharp(cnf, smooth=True)


def _compile_with_dsharp(cnf: CNF, smooth=True):
    result = None
    fd1, cnf_file = tempfile.mkstemp(".cnf")
    fd2, nnf_file = tempfile.mkstemp(".nnf")
    os.close(fd1)
    os.close(fd2)
    if smooth:
        smoothl = ["-smoothNNF"]
    else:
        smoothl = []
    cmd = ["dsharp", "-Fnnf", nnf_file] + smoothl + ["-disableAllLits", cnf_file]  #

    try:
        result = _compile(cnf, cmd, cnf_file, nnf_file)
    except subprocess.CalledProcessError as err:
        raise err
    finally:
        try:
            os.remove(cnf_file)
        except OSError:
            pass
        try:
            os.remove(nnf_file)
        except OSError:
            pass
    return result


def _compile(cnf: CNF, cmd, cnf_file: str, nnf_file: str):
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


def _load_nnf(filename: str) -> DDNNF:
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
        # assert len(line2idx) == num_literal_nodes * 2,  # not true, but I guess if it is not used then no need to have it in line2idx
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
                if len(children) > 0:
                    # for some reason with mc2023_track2_000, there is an A 0 without children.
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
