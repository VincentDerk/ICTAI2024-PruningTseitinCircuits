import os
import subprocess
import sys
import pickle
import string
import time

from graphviz import Source

# To use ../core/ imports, we are adding the parent folder to sys.path
script_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.append(parent_dir)

from core.cnf import CNF
from core.cnf2ddnnf import cnf_to_ddnnf
from core.ddnnf import DDNNF
from core.ddnnf_extra import compress_ddnnf, smooth_ddnnf, existential_quantification, \
    existential_quantification_tseitin, compute_nb_operations, ddnnf_to_dot
from core.varinfo import VariableSetInfo
from problog_analysis.problog2ddnnf import  logicdag_to_cnf

from problog.formula import LogicDAG
from problog.program import PrologFile
from problog.engine import DefaultEngine


def _compile_instance(cnf: CNF, timeout) -> (DDNNF, int, str):
    """ returns d-DNNF, compile time, var_info and status """
    ddnnf = None
    compile_time = 0
    try:
        ddnnf, compile_time = cnf_to_ddnnf(cnf, timeout=timeout)
        status = "success"
    except subprocess.CalledProcessError as err:
        print(err, file=sys.stderr)
        status = "failed"
    except subprocess.TimeoutExpired as err:
        print(f"Timeout error when compiling. Skipped it.")
        status = "timeout"
    except MemoryError as err:
        print(f"Memory error. Skipped it.")
        status = "memory_error"
    return ddnnf, compile_time, status


def _generate_result_csv(result_csv_path):
    if not os.path.exists(result_csv_path):
        os.makedirs(os.path.dirname(result_csv_path), exist_ok=True)
        # instance name + information
        # compile time
        # ddnnf node count (after smoothing)
        # ddnnf node count after existential quantification of tseitin variables (after smoothing)
        # ddnnf node count after removing tseitin artifacts (+ adding smoothing nodes)
        # NOTE: node count includes atoms. To exclude these, subtract var_count from it
        with open(result_csv_path, "w+") as f:
            f.write("filepath,var_count,tseitin_var_count,compile_time,"
                    "ddnnf_nodecount_plus,ddnnf_nodecount_mult,"
                    "sddnnf_nodecount_plus,sddnnf_nodecount_mult,"
                    "ddnnf_exist_nodecount_plus,ddnnf_exist_nodecount_mult,"
                    "sddnnf_exist_nodecount_plus,sddnnf_exist_nodecount_mult,"
                    "ddnnf_tseitin_nodecount_plus,ddnnf_tseitin_nodecount_mult,"
                    "sddnnf_tseitin_nodecount_plus,sddnnf_tseitin_nodecount_mult\n")


def _write_to_result_csv(result_csv_path: str, result: dict):
    instance_name = result["filepath"]
    var_count = result["var_count"]
    tseitin_var_count = result["tseitin_var_count"]
    compile_time = result["compile_time"]
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
        f.write(f"{instance_name},{var_count},{tseitin_var_count},{compile_time:.3f},"
                f"{ddnnf_nodecount_plus},{ddnnf_nodecount_mult},"
                f"{sddnnf_nodecount_plus},{sddnnf_nodecount_mult},"
                f"{ddnnf_exist_nodecount_plus},{ddnnf_exist_nodecount_mult},"
                f"{sddnnf_exist_nodecount_plus},{sddnnf_exist_nodecount_mult},"
                f"{ddnnf_tseitin_nodecount_plus},{ddnnf_tseitin_nodecount_mult},"
                f"{sddnnf_tseitin_nodecount_plus},{sddnnf_tseitin_nodecount_mult}\n")


def _process(result_csv_path, instance_filepath):
    model = PrologFile(instance_filepath)
    engine = DefaultEngine(label_all=True)
    db = engine.prepare(model)
    gp = engine.ground_all(db)
    gp = LogicDAG.createFrom(gp)
    cnf, var_info = logicdag_to_cnf(gp, add_query=True)
    print(f"\tCNF of vars {cnf.var_count} with {cnf.clause_count()} clauses and "
          f"{len(var_info.tseitin_vars)} ({(len(var_info.tseitin_vars) / cnf.var_count * 100):.1f}%) "
          f"Tseitin variables.")

    # if cnf.var_count < 100 or len(var_info.tseitin_vars) < 10:
    #     print(f"\tSkipped instance {instance_filepath}")
    #     return

    result_dict = dict()
    result_dict["filepath"] = instance_filepath

    print(f"\tCompiling instance {instance_filepath}")
    ddnnf, compile_time, status = _compile_instance(cnf, timeout=3600)
    result_dict["compile_time"] = compile_time
    result_dict["var_count"] = ddnnf.var_count if ddnnf is not None else 0
    result_dict["tseitin_var_count"] = len(var_info.tseitin_vars) if var_info is not None else 0
    print(f"\tCompiled {instance_filepath} with {status} and compile time {compile_time:.3f}s.")

    Source(ddnnf_to_dot(ddnnf, None)).render(view=True)
    if ddnnf is not None and status == "success":
        # compress d-DNNF
        ddnnf = compress_ddnnf(ddnnf)

        # simple existential quantification of tseitin variables
        start_time = time.time()
        ddnnfp = existential_quantification(ddnnf, var_info.tseitin_vars)
        end_time = time.time()
        nb_plus, nb_times = compute_nb_operations(ddnnfp)
        print(
            f"\tExistential quantification took {(end_time - start_time):.3f}s. + ({nb_plus}) * ({nb_times})")

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
        result_dict["sddnnf_tseitin_nodecount_plus"] = "NA"
        result_dict["sddnnf_tseitin_nodecount_mult"] = "NA"


def execute_experiment(result_csv_path, problog_folder_dir):
    _generate_result_csv(result_csv_path)
    for filename in os.listdir(problog_folder_dir):
        instance_filepath = os.path.join(problog_folder_dir, filename)
        print(f"Processing {instance_filepath}")
        _process(result_csv_path, instance_filepath)


def temp_get_cnf(instance_filepath):
    model = PrologFile(instance_filepath)
    engine = DefaultEngine(label_all=True)
    db = engine.prepare(model)
    gp = engine.ground_all(db)
    gp = LogicDAG.createFrom(gp)
    cnf, var_info = logicdag_to_cnf(gp, add_query=True)
    print(f"\tCNF of vars {cnf.var_count} with {cnf.clause_count()} clauses and "
          f"{len(var_info.tseitin_vars)} ({(len(var_info.tseitin_vars) / cnf.var_count * 100):.1f}%) "
          f"Tseitin variables.")
    cnf_file = "./andes_20240614.net.cnf"
    # write dimacs
    with open(cnf_file, "w") as f:
        f.write(cnf.to_dimacs())
        f.write(f"\nc p auxilliary {' '.join((str(x) for x in var_info.tseitin_vars))}")


if __name__ == "__main__":
    # result_path = "./results/bn_exp.csv"
    # folder_dir = "../sources/problog_bn_query/"
    # execute_experiment(result_path, folder_dir)
    # temp_get_cnf("../sources/problog_bn_query_no_tseitin/andes-noneg.net.pl")
    # _process("./results/temp.csv", "../sources/problog_bn_query_no_tseitin/andes-noneg.net.pl")
    _process("./results/temp.csv", "./temp-noisy-2.pl")

