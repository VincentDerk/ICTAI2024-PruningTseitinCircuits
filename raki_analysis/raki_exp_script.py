import os
import pickle
import resource
import subprocess
import sys
import time

# To use ../core/ imports, we are adding the parent folder to sys.path
script_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.append(parent_dir)

from cnf_analysis.cnf2tseitin import determine_tseitin_from_cnf

from core.cnf import read_cnf
from core.cnf2ddnnf import cnf_to_ddnnf
from core.ddnnf import DDNNF
from core.varinfo import VariableSetInfo
from core.ddnnf_evaluator import DDNNFTraverserBottomUp
from core.ddnnf_extra import existential_quantification, smooth_ddnnf, \
    existential_quantification_tseitin, compress_ddnnf


def _compile_instance(cnf_filepath: str, timeout) -> (DDNNF, int, str):
    """ returns d-DNNF, compile time and status """
    ddnnf = None
    compile_time = 0
    cnf = read_cnf(cnf_filepath)
    try:
        ddnnf, compile_time = cnf_to_ddnnf(cnf, timeout=timeout)
        status = "success"
    except subprocess.CalledProcessError as err:
        print(err, file=sys.stderr)
        status = "failed"
    except subprocess.TimeoutExpired as err:
        print(f"Timeout error when compiling {cnf_filepath}. Skipped it.")
        status = "timeout"
    except MemoryError as err:
        print(f"Memory error when compiling / after loading in d-DNNF for {cnf_filepath}. Skipped it.")
        status = "memory_error"
    return ddnnf, compile_time, status


def _generate_result_csv(result_csv_path):
    if not os.path.exists(result_csv_path):
        os.makedirs(os.path.dirname(result_csv_path), exist_ok=True)

        # cnf + information
        # compile time + when compiled?
        # ddnnf node count (after smoothing)
        # ddnnf node count after existential quantification of tseitin variables (after smoothing)
        # ddnnf node count after removing tseitin artifacts (+ adding smoothing nodes)
        # NOTE: node count includes atoms. To exclude these, subtract var_count from it
        with open(result_csv_path, "w+") as f:
            f.write("cnf_path,clause_count,var_count,tseitin_var_count,"
                    "compile_time,timestamp,"
                    "ddnnf_nodecount_plus,ddnnf_nodecount_mult,"
                    "sddnnf_nodecount_plus,sddnnf_nodecount_mult,"
                    "ddnnf_exist_nodecount_plus,ddnnf_exist_nodecount_mult,"
                    "sddnnf_exist_nodecount_plus,sddnnf_exist_nodecount_mult,"
                    "ddnnf_tseitin_nodecount_plus,ddnnf_tseitin_nodecount_mult,"
                    "sddnnf_tseitin_nodecount_plus,sddnnf_tseitin_nodecount_mult\n")


def _write_to_result_csv(result_csv_path: str, result: dict):
    cnf_path = result["cnf_path"]
    clause_count = result["clause_count"]
    var_count = result["var_count"]
    tseitin_var_count = result["tseitin_var_count"]
    compile_time = result["compile_time"]
    timestamp = result["timestamp"]
    ddnnf_nodecount_plus = result["ddnnf_nodecount_plus"]
    ddnnf_nodecount_mult = result["ddnnf_nodecount_mult"]
    sddnnf_nodecount_plus = result["sddnnf_nodecount_plus"]
    sddnnf_nodecount_mult = result["sddnnf_nodecount_mult"]
    ddnnf_exist_nodecount_plus = result["ddnnf_exist_nodecount_plus"]
    ddnnf_exist_nodecount_mult = result["ddnnf_exist_nodecount_mult"]
    sddnnf_exist_nodecount_plus = result["sddnnf_exist_nodecount_plus"]
    sddnnf_exist_nodecount_mult = result["sddnnf_exist_nodecount_mult"]
    ddnnf_tseitin_nodecount_plus = result["ddnnf_tseitin_nodecount_plus"]
    ddnnf_tseitin_nodecount_mult = result["ddnnf_tseitin_nodecount_mult"]
    sddnnf_tseitin_nodecount_plus = result["sddnnf_tseitin_nodecount_plus"]
    sddnnf_tseitin_nodecount_mult = result["sddnnf_tseitin_nodecount_mult"]
    with open(result_csv_path, "a") as f:
        f.write(f"{cnf_path},{clause_count},{var_count},{tseitin_var_count},"
                f"{compile_time:.3f},{timestamp},"
                f"{ddnnf_nodecount_plus},{ddnnf_nodecount_mult},"
                f"{sddnnf_nodecount_plus},{sddnnf_nodecount_mult},"
                f"{ddnnf_exist_nodecount_plus},{ddnnf_exist_nodecount_mult},"
                f"{sddnnf_exist_nodecount_plus},{sddnnf_exist_nodecount_mult},"
                f"{ddnnf_tseitin_nodecount_plus},{ddnnf_tseitin_nodecount_mult},"
                f"{sddnnf_tseitin_nodecount_plus},{sddnnf_tseitin_nodecount_mult}\n")


def _finished_cnfs(result_csv_path):
    finished_instances = set()
    with open(result_csv_path, "r") as f:
        for line in f.readlines()[1:]:
            line = line.split(",")
            instance_path = line[0]
            finished_instances.add(instance_path)
    return finished_instances


def _read_instance_list(csv_filepath):
    instances = list()
    with open(csv_filepath, "r") as f:
        for line in f.readlines()[1:]:
            line = line.split(",")
            instance_path = line[0]
            instances.append(instance_path)
    return instances


def _get_varinfo(cnf_instance_filepath: str) -> (int, int, VariableSetInfo):
    tseitin_vars = set()
    with open(cnf_instance_filepath, "r") as f:
        for line in f.readlines():
            if line.startswith("p cnf"):
                line_block = line.split(" ")
                assert len(line_block) == 4
                var_count = int(line_block[2])
                clause_count = int(line_block[3])
            elif line.startswith("c p auxilliary"):
                offset = len("c p auxilliary ")
                line = line[offset:]
                line = line[:-3]  # remove newline and the trailing  0 guard
                tseitin_vars = set(int(v) for v in line.split(" "))

    var_info = VariableSetInfo(tseitin_vars=tseitin_vars)
    assert len(tseitin_vars) > 0, "No tseitin variables detected, why create this?"
    assert len(tseitin_vars) < var_count, "Tseitin variables must be a subset of all variables"
    return var_count, clause_count, var_info


def compute_nb_operations(ddnnf: DDNNF, include_unused_vars=False) -> (int, int):
    """
    Compute the number of addition and multiplication operations within the given ddnnf.
    This method uses a bottom-up traversal.
    :param ddnnf: The d-DNNF in which to compute the number of operations.
    :param include_unused_vars: If true, we treat every unused var as a smoothing operation.
    :return: The number of addition and multiplication operations (as a tuple) in ddnnf.
        A non-binary operation is reduced to a binary one, e.g., +(a,b,c) counts as two +.
    """
    nb_plus = 0
    nb_times = 0
    traversor = DDNNFTraverserBottomUp(ddnnf)
    for node_idx, node in traversor.next_node():
        if node.node_type == "disj":
            nb_plus += len(node.node_field) - 1
        elif node.node_type == "conj":
            nb_times += len(node.node_field) - 1
    if include_unused_vars:
        nb_plus += len(ddnnf.unused_vars)
        nb_times += len(ddnnf.unused_vars)  # n-1 for unused vars +1 product with root node.
    return nb_plus, nb_times


def _process(instance_filepath, result_csv_path, timeout):
    result_dict = dict()
    result_dict["cnf_path"] = instance_filepath

    #   extract cnf and varinfo from instance
    var_count, clause_count, var_info = _get_varinfo(instance_filepath)
    tseitin_var_count = len(var_info.tseitin_vars)
    result_dict["var_count"] = var_count
    result_dict["clause_count"] = clause_count
    result_dict["tseitin_var_count"] = tseitin_var_count
    print(f"Handling {instance_filepath}; vars={var_count}; clauses={clause_count}; tseitin_vars={tseitin_var_count} ({(tseitin_var_count / var_count *100):.2f}%)")

    #   compile instance to ddnnf
    ddnnf, compile_time, status = _compile_instance(instance_filepath, timeout=timeout)
    result_dict["compile_time"] = compile_time
    result_dict["timestamp"] = time.time()
    print(f"\tCompiled {instance_filepath} with {status} and compile time {compile_time:.3f}s.")

    if ddnnf is not None and status == "success":
        # compress d-DNNF
        ddnnf = compress_ddnnf(ddnnf)

        # ddnnf_nodecount
        nb_plus, nb_times = compute_nb_operations(ddnnf)
        print(f"\td-DNNF after compression. + ({nb_plus}) * ({nb_times})")
        result_dict["ddnnf_nodecount_plus"] = nb_plus
        result_dict["ddnnf_nodecount_mult"] = nb_times

        # sddnnf_nodecount
        start_time = time.time()
        sddnnf = smooth_ddnnf(ddnnf)
        end_time = time.time()
        nb_plus, nb_times = compute_nb_operations(sddnnf, include_unused_vars=True)
        print(f"\tSmoothing took {(end_time - start_time):.3f}s. + ({nb_plus}) * ({nb_times})")
        del sddnnf
        result_dict["sddnnf_nodecount_plus"] = nb_plus
        result_dict["sddnnf_nodecount_mult"] = nb_times

        # simple existential quantification of tseitin variables
        start_time = time.time()
        ddnnfp = existential_quantification(ddnnf, var_info.tseitin_vars)
        end_time = time.time()
        nb_plus, nb_times = compute_nb_operations(ddnnfp)
        print(
            f"\tExistential quantification took {(end_time - start_time):.3f}s. + ({nb_plus}) * ({nb_times})")
        result_dict["ddnnf_exist_nodecount_plus"] = nb_plus
        result_dict["ddnnf_exist_nodecount_mult"] = nb_times

        # smoothing simple existential quantification of tseitin variables
        sddnnfp = smooth_ddnnf(ddnnfp)
        del ddnnfp
        nb_plus, nb_times = compute_nb_operations(sddnnfp, include_unused_vars=True)
        print(f"\tSmoothing after simple existential quantification. + ({nb_plus}) * ({nb_times})")
        del sddnnfp
        result_dict["sddnnf_exist_nodecount_plus"] = nb_plus
        result_dict["sddnnf_exist_nodecount_mult"] = nb_times

        # tseitin-artifact removal + existential quantification
        start_time = time.time()
        ddnnft = existential_quantification_tseitin(ddnnf, var_info.tseitin_vars)
        del ddnnf
        end_time = time.time()
        nb_plus, nb_times = compute_nb_operations(ddnnft)
        print(
            f"\tExistential quantification witth Tseitin took {(end_time - start_time):.3f}s. + ({nb_plus}) * ({nb_times})")
        result_dict["ddnnf_tseitin_nodecount_plus"] = nb_plus
        result_dict["ddnnf_tseitin_nodecount_mult"] = nb_times

        # smooth tseitin ddnnf
        sddnnft = smooth_ddnnf(ddnnft)
        del ddnnft
        nb_plus, nb_times = compute_nb_operations(sddnnft, include_unused_vars=True)
        del sddnnft
        print(f"\tSmooth after Tseitin. + ({nb_plus}) * ({nb_times})")
        result_dict["sddnnf_tseitin_nodecount_plus"] = nb_plus
        result_dict["sddnnf_tseitin_nodecount_mult"] = nb_times

    elif status == "timeout" or status == "memory_error":
        err_msg = "TO" if status == "timeout" else "MEM_ERR"
        result_dict["ddnnf_nodecount_plus"] = err_msg
        result_dict["ddnnf_nodecount_mult"] = err_msg
        result_dict["ddnnf_exist_nodecount_plus"] = err_msg
        result_dict["ddnnf_exist_nodecount_mult"] = err_msg
        result_dict["ddnnf_tseitin_nodecount_plus"] = err_msg
        result_dict["ddnnf_tseitin_nodecount_mult"] = err_msg
        result_dict["sddnnf_nodecount_plus"] = err_msg
        result_dict["sddnnf_nodecount_mult"] = err_msg
        result_dict["sddnnf_exist_nodecount_plus"] = err_msg
        result_dict["sddnnf_exist_nodecount_mult"] = err_msg
        result_dict["sddnnf_tseitin_nodecount_plus"] = err_msg
        result_dict["sddnnf_tseitin_nodecount_mult"] = err_msg

    if status == "success" or status == "timeout" or status == "memory_error":
        _write_to_result_csv(result_csv_path, result_dict)
    # else: we printed the error and should look into this instance.


def execute_experiment(cnf_folder_path, result_csv_path, timeout=600):
    MAX_VMEMORY = 24 * 1024 * 1024 * 1024  # 4GB (in bytes)
    resource.setrlimit(resource.RLIMIT_AS, (MAX_VMEMORY, resource.RLIM_INFINITY))

    _generate_result_csv(result_csv_path)
    for filename in os.listdir(cnf_folder_path):
        if filename.endswith("cnf"):
            instance_filepath = os.path.join(cnf_folder_path, filename)
            print(f"Processing {instance_filepath}")
            _process(instance_filepath, result_csv_path, timeout=timeout)


if __name__ == "__main__":
    result_csv = "results/results_cnf_exp.csv"
    _timeout = 600
    _process("../sources/raki_aux_benchmarks/gh/gh_2_prob.lp.cnf", result_csv, timeout=_timeout)
    # execute_experiment("../sources/raki_aux_benchmarks/gh/", result_csv, timeout=_timeout)
    # execute_experiment("../sources/raki_aux_benchmarks/gnb/", result_csv, timeout=_timeout)
    # execute_experiment("../sources/raki_aux_benchmarks/lp2sat/", result_csv, timeout=_timeout)
    # execute_experiment("../sources/raki_aux_benchmarks/smokers/", result_csv, timeout=_timeout)
    # execute_experiment("../sources/raki_aux_benchmarks/tree/", result_csv, timeout=_timeout)

