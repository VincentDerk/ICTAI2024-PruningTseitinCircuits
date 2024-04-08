import os
import resource
import subprocess
import tempfile
import time

from core.cnf import CNF
from core.ddnnf import DDNNF


def cnf_to_ddnnf(cnf: CNF, k="D4", timeout=600) -> (DDNNF, int):
    """ Returns ddnnf and compile time
    Relevant exceptions: subprocess.CalledProcessError, subprocess.TimeoutExpired and MemoryError.
    """
    if k == "dsharp":
        return _compile_with_dsharp(cnf, smooth=True)
    else:
        return _compile_with_d4(cnf, timeout=timeout)


def _compile_with_d4(cnf: CNF, timeout):
    result = None
    compile_time = 0
    fd1, cnf_file = tempfile.mkstemp(".cnf")
    fd2, nnf_file = tempfile.mkstemp(".nnf")
    os.close(fd1)
    os.close(fd2)
    # cmd = f"ulimit -S -m $((3*1024*1024)) && ../bin/d4_static {cnf_file} -dDNNF -out={nnf_file}"
    cmd = ["../bin/d4_static", cnf_file, "-dDNNF", "-rnd-seed=458834", f"-out={nnf_file}"]

    def _set_mem_resources():
        MAX_VIRTUAL_MEMORY = 64 * 1024 * 1024 * 1024  # 4GB (in bytes)
        resource.setrlimit(resource.RLIMIT_AS, (MAX_VIRTUAL_MEMORY, resource.RLIM_INFINITY))
        # resource.setrlimit(resource.RLIMIT_DATA, (MAX_VIRTUAL_MEMORY, resource.RLIM_INFINITY))
        # resource.setrlimit(resource.RLIMIT_STACK, (MAX_VIRTUAL_MEMORY, resource.RLIM_INFINITY))

    try:
        # write dimacs
        with open(cnf_file, "w") as f:
            f.write(cnf.to_dimacs())

        # call compiler
        start_time = time.time()
        result = subprocess.run(cmd, shell=False, check=True, stdout=subprocess.DEVNULL,
                                timeout=timeout, preexec_fn=_set_mem_resources)
        end_time = time.time()
        compile_time = end_time - start_time
        success = result.returncode == 0
        if not success:
            raise Exception(f"D4 subprocess failed {cmd}")

        # load result
        result = _load_nnf_d4(nnf_file, cnf.var_count)
    except subprocess.CalledProcessError as err:
        raise err
    except subprocess.TimeoutExpired as err:
        raise err
    except MemoryError as err:
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
    return result, compile_time


def _load_nnf_d4(filepath: str, num_vars) -> DDNNF:
    # we assume node 1 is the root node.
    # each node has a node_type definition, appearing before listing its edges.
    with open(filepath) as f:
        # first we create an intermediate structure of D4's NNF graph,
        # combining the information of each or/and node.
        nnf_graph_d4 = [None]
        node_types = [None]

        def _add_node_type(_node_type, _node_idx):
            if _node_idx >= len(node_types):
                extend_with_nb = _node_idx - len(node_types) + 1
                node_types.extend((None for _ in range(extend_with_nb)))
            if _node_idx >= len(nnf_graph_d4):
                extend_with_nb = _node_idx - len(nnf_graph_d4) + 1
                nnf_graph_d4.extend((None for _ in range(extend_with_nb)))
            node_types[_node_idx] = _node_type

        def _add_or_node(_curr_node_idx, _child_node_idx, _implied_literals):
            if _curr_node_idx >= len(nnf_graph_d4):
                extend_with_nb = _curr_node_idx - len(nnf_graph_d4) + 1
                nnf_graph_d4.extend((None for _ in range(extend_with_nb)))
            if nnf_graph_d4[_curr_node_idx] is None:
                nnf_graph_d4[_curr_node_idx] = list()
            if node_types[_child_node_idx] != "f":
                # if child node is false, then we do not add it to the or node.
                # this will then become an or node with one child
                # which is treated as an AND node during construction into d-DNNF (below).
                nnf_graph_d4[_curr_node_idx].append((_child_node_idx, _implied_literals))

        def _add_and_node(_curr_node_idx, _child_node_idx):
            if _curr_node_idx >= len(nnf_graph_d4):
                extend_with_nb = _curr_node_idx - len(nnf_graph_d4) + 1
                nnf_graph_d4.extend((None for _ in range(extend_with_nb)))
            if nnf_graph_d4[_curr_node_idx] is None:
                nnf_graph_d4[_curr_node_idx] = list()
            nnf_graph_d4[_curr_node_idx].append(child_node_idx)

        assert len(nnf_graph_d4) == len(node_types)

        for line in f.readlines():
            # print(line)
            line = line[:-2].strip().split()
            node_type = line[0]
            is_node_def = node_type in ("o", "a", "t", "f")
            if is_node_def:
                node_idx = int(line[1])
                _add_node_type(node_type, node_idx)
            else:
                node_idx = int(line[0])
                if node_types[node_idx] == "o":
                    curr_node_idx = int(line[0])
                    child_node_idx = int(line[1])
                    implied_lits = {int(lit) for lit in line[2:]}
                    assert all(abs(lit) <= num_vars for lit in implied_lits)
                    _add_or_node(curr_node_idx, child_node_idx, implied_lits)
                else:
                    assert len(line) == 2
                    curr_node_idx = int(line[0])
                    child_node_idx = int(line[1])
                    _add_and_node(curr_node_idx, child_node_idx)

        # now we create the ddnnf recursively.
        node_map = [None] * len(nnf_graph_d4)
        ddnnf = DDNNF()
        for atom in range(1, num_vars+1):
            ddnnf.add_atom(atom)

        # recursive DFS annotation starting from node 1
        def _recursive_complete_ddnnf(d4_idx):
            if node_map[d4_idx] is not None:  # check cache
                return node_map[d4_idx]

            node_type = node_types[d4_idx]

            if node_type == "t":
                return -1
            elif node_type == "f":
                return 0
            elif node_type == "o":
                node_info = nnf_graph_d4[d4_idx]
                if len(node_info) == 1:
                    child, implied_literals = node_info[0]
                    if len(implied_literals) == 0:
                        return _recursive_complete_ddnnf(child)
                    else:
                        child1 = _recursive_complete_ddnnf(child)
                        children = (child1,) + tuple(implied_literals)
                        and_ddnnf_node = ddnnf.add_conj(children)
                        node_map[d4_idx] = and_ddnnf_node
                        return and_ddnnf_node

                assert len(node_info) == 2
                child1, implied_literals1 = node_info[0]
                child2, implied_literals2 = node_info[1]
                mapped_child1 = _recursive_complete_ddnnf(child1)
                mapped_child2 = _recursive_complete_ddnnf(child2)

                # if any child is True; replace with True
                # if any child is False; replace with the other child
                # TODO: Then we might need to clean up previous nodes?

                # create and node 1
                if mapped_child1 > 0:
                    children1 = (mapped_child1,) + tuple(implied_literals1)
                else:
                    assert mapped_child1 == -1, "Did not expect false."
                    children1 = tuple(implied_literals1)
                if len(children1) == 1:
                    child_ddnnf_node1 = children1[0]
                else:
                    child_ddnnf_node1 = ddnnf.add_conj(children1)

                # create and node 2
                if mapped_child2 > 0:
                    children2 = (mapped_child2,) + tuple(implied_literals2)
                else:
                    assert mapped_child2 == -1, "Did not expect false"
                    children2 = tuple(implied_literals2)
                if len(children2) == 1:
                    child_ddnnf_node2 = children2[0]
                else:
                    child_ddnnf_node2 = ddnnf.add_conj(children2)
                # combine and nodes into or node
                or_ddnnf_node = ddnnf.add_disj((child_ddnnf_node1, child_ddnnf_node2))
                node_map[d4_idx] = or_ddnnf_node
                return or_ddnnf_node

            elif node_type == "a":
                # create and node and return it.
                children = nnf_graph_d4[d4_idx]
                assert len(children) > 1
                mapped_children = []
                for child in children:
                    mapped_child = _recursive_complete_ddnnf(child)
                    assert mapped_child > 0
                    mapped_children.append(mapped_child)
                and_node_ddnnf = ddnnf.add_conj(tuple(mapped_children))
                node_map[d4_idx] = and_node_ddnnf
                return and_node_ddnnf

        final_idx = _recursive_complete_ddnnf(1)
        # TODO: if final_idx is 0 then ddnnf must represent False.
        # TODO: if final_idx is -1, then ddnnf must represent True.
        assert final_idx > 0
        return ddnnf


def _compile_with_dsharp(cnf: CNF, smooth=True):
    result = None
    compile_time = 0
    fd1, cnf_file = tempfile.mkstemp(".cnf")
    fd2, nnf_file = tempfile.mkstemp(".nnf")
    os.close(fd1)
    os.close(fd2)
    if smooth:
        smoothl = ["-smoothNNF"]
    else:
        smoothl = []
    cmd = ["../bin/dsharp", "-Fnnf", nnf_file] + smoothl + ["-disableAllLits", cnf_file]  #

    try:
        # write dimacs
        with open(cnf_file, "w") as f:
            f.write(cnf.to_dimacs())

        # call compiler
        start_time = time.time()
        result = subprocess.run(cmd, shell=False, check=True, stdout=subprocess.DEVNULL)
        end_time = time.time()
        compile_time = end_time - start_time
        success = result.returncode == 0
        if not success:
            raise Exception(f"dSharp subprocess failed {cmd}")

        # load result
        result = _load_nnf(nnf_file)
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
    return result, compile_time


def _load_nnf(filename: str) -> DDNNF:
    """ NNF from dsharp """
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

