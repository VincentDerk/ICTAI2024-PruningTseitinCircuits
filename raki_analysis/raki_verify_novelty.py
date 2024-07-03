#!/usr/bin/env python3
import sys
import tempfile
import os

from aspmc.compile.cnf import CNF
import aspmc.compile.dtree as dtree
import aspmc.main

from aspmc.config import config

from core.ddnnf import DDNNF
from core.ddnnf_evaluator import compute_model_count
from core.ddnnf_extra import compute_nb_operations, compress_ddnnf, \
    existential_quantification_tseitin


def _load_nnf(filename):
    nnf = DDNNF()

    with open(filename, "r") as f:
        line2node = {}  # stores line number to node.
        rename = {}  # stores Literal ID to node id . Literal ID may differ from line number
        lnum = 0
        for line in f:
            line = line.strip().split()
            if line[0] == "nnf":
                pass
            elif line[0] == "L":
                literal = int(line[1])
                variable = abs(literal)
                if variable not in rename:
                    # store atom in rename such that Literal ID maps to a node.
                    pos_node_idx = nnf.add_atom(variable)
                    neg_node_idx = -pos_node_idx
                    rename[variable] = pos_node_idx
                    rename[-variable] = neg_node_idx
                # complete line2node based on rename dictionary.
                line2node[lnum] = rename[literal]
                lnum += 1
            elif line[0] == "A":
                children = [line2node[int(x)] for x in line[2:]]
                line2node[lnum] = nnf.add_conj(children)
                lnum += 1
            elif line[0] == "O":
                children = [line2node[int(x)] for x in line[3:]]
                line2node[lnum] = nnf.add_disj(children)
                lnum += 1
            else:
                print("Unknown line type")
    return nnf


# sharpsat-td-mfg based on https://github.com/raki123/KC-benchmarking/blob/main/aux_compile.py
config["decot"] = "10"
cnf_filepath = "../sources/raki_aux_benchmarks/smokers/smokers_9_2_prob.lp.cnf"  # mc = 536870912
cnf = CNF(cnf_filepath)

cnf_fd, cnf_tmp = tempfile.mkstemp()
with os.fdopen(cnf_fd, 'wb') as cnf_file:
    cnf.write_kc_cnf(cnf_file)
CNF.compile_single(cnf_tmp, knowledge_compiler="sharpsat-td")
print(cnf_tmp)
ddnnf = _load_nnf(cnf_tmp + ".nnf")
os.remove(cnf_tmp)
os.remove(cnf_tmp + ".nnf")

# compute stuff
nb_plus, nb_times = compute_nb_operations(ddnnf)
node_count = nb_plus + nb_times
print(f"\td-DNNF before compression. + ({nb_plus}) * ({nb_times})")
mc = compute_model_count(ddnnf)
print(f"Model count: {mc}")
assert mc == 536870912, f"The model count for smokers/smokers_9_2prob.lp.cnf is 536870912 according to D4. We instead found {mc}. \n Perhaps we messed up load_nnf(...)?"

# compress
ddnnf = compress_ddnnf(ddnnf)
nb_plus, nb_times = compute_nb_operations(ddnnf)
node_count2 = nb_plus + nb_times
print(f"\td-DNNF after compression. + ({nb_plus}) * ({nb_times})")
mc = compute_model_count(ddnnf)
assert mc == 536870912, f"The model count for smokers/smokers_9_2prob.lp.cnf is 536870912 according to D4. We instead found {mc}"

# existential quantification to find any tseitin
ddnnft = existential_quantification_tseitin(ddnnf, tseitin_vars=set())
nb_plus, nb_times = compute_nb_operations(ddnnft)
node_count3 = nb_plus + nb_times
print(f"\tExistential quantification witth Tseitin: + ({nb_plus}) * ({nb_times})")
if node_count3 < node_count2:
    print("TEST SUCCESFUL!")
    print("Tseitin removal reduces the formula from sharpsat-td-mfg, so they did not yet implement this optimization.")
else:
    assert False, f"We expect sharpsat-td-mfg to not yet remove tseitin artifacts, so we expected {node_count3} < {node_count2}"



