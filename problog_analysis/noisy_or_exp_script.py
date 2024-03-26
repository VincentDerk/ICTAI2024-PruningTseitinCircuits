import os
import subprocess
import sys
import time

from problog.program import PrologString

from cnf_analysis.cnf_exp_script import _compute_nb_operations
from core.ddnnf import DDNNF
from core.ddnnf_extra import compress_ddnnf, smooth_ddnnf, existential_quantification, \
    existential_quantification_tseitin
from core.varinfo import VariableSetInfo
from problog_analysis.problog2ddnnf import problog_model_to_ddnnf


def _compile_instance(model: PrologString, timeout) -> (DDNNF, int, VariableSetInfo, str):
    """ returns d-DNNF, compile time, var_info and status """
    ddnnf = None
    compile_time = 0
    var_info = None
    try:
        ddnnf, compile_time, var_info = problog_model_to_ddnnf(model, timeout=timeout)
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
    return ddnnf, compile_time, var_info, status


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
            f.write("instance_name,tseitin_var_count,compile_time,"
                    "ddnnf_nodecount_plus,ddnnf_nodecount_mult,"
                    "sddnnf_nodecount_plus,sddnnf_nodecount_mult,"
                    "ddnnf_exist_nodecount_plus,ddnnf_exist_nodecount_mult,"
                    "sddnnf_exist_nodecount_plus,sddnnf_exist_nodecount_mult,"
                    "ddnnf_tseitin_nodecount_plus,ddnnf_tseitin_nodecount_mult,"
                    "sddnnf_tseitin_nodecount_plus,sddnnf_tseitin_nodecount_mult\n")


def _write_to_result_csv(result_csv_path: str, result: dict):
    instance_name = result["instance_name"]
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
        f.write(f"{instance_name},{tseitin_var_count},{compile_time:.3f},"
                f"{ddnnf_nodecount_plus},{ddnnf_nodecount_mult},"
                f"{sddnnf_nodecount_plus},{sddnnf_nodecount_mult},"
                f"{ddnnf_exist_nodecount_plus},{ddnnf_exist_nodecount_mult},"
                f"{sddnnf_exist_nodecount_plus},{sddnnf_exist_nodecount_mult},"
                f"{ddnnf_tseitin_nodecount_plus},{ddnnf_tseitin_nodecount_mult},"
                f"{sddnnf_tseitin_nodecount_plus},{sddnnf_tseitin_nodecount_mult}\n")


def _generate_noisy_or_str_instance(nb_parents):
    noisy_or_str = ""
    for i in range(nb_parents):
        noisy_or_str += f"0.5::a({i}). "
    noisy_or_str += ("0.25::aux(X).\n"
                     "x :- a(X), aux(X).\n"
                     "query(x).")
    return noisy_or_str


def _execute_noisy_or(result_csv_path, model, instance_name):
    result_dict = dict()
    result_dict["instance_name"] = instance_name

    print(f"Compiling instance {instance_name}")
    ddnnf, compile_time, var_info, status = _compile_instance(model, timeout=600)
    result_dict["compile_time"] = compile_time
    result_dict["tseitin_var_count"] = len(var_info.tseitin_vars) if var_info is not None else 0
    print(f"\tCompiled {instance_name} with {status} and compile time {compile_time:.3f}s.")

    if ddnnf is not None and status == "success":
        # compress d-DNNF
        ddnnf = compress_ddnnf(ddnnf)

        # ddnnf_nodecount
        nb_plus, nb_times = _compute_nb_operations(ddnnf)
        print(f"\td-DNNF after compression. + ({nb_plus}) * ({nb_times})")
        result_dict["ddnnf_nodecount_plus"] = nb_plus
        result_dict["ddnnf_nodecount_mult"] = nb_times

        # sddnnf_nodecount
        start_time = time.time()
        sddnnf = smooth_ddnnf(ddnnf)
        end_time = time.time()
        nb_plus, nb_times = _compute_nb_operations(sddnnf, include_unused_vars=True)
        print(f"\tSmoothing took {(end_time - start_time):.3f}s. + ({nb_plus}) * ({nb_times})")
        del sddnnf
        result_dict["sddnnf_nodecount_plus"] = nb_plus
        result_dict["sddnnf_nodecount_mult"] = nb_times

        # simple existential quantification of tseitin variables
        start_time = time.time()
        ddnnfp = existential_quantification(ddnnf, var_info.tseitin_vars)
        end_time = time.time()
        nb_plus, nb_times = _compute_nb_operations(ddnnfp)
        print(
            f"\tExistential quantification took {(end_time - start_time):.3f}s. + ({nb_plus}) * ({nb_times})")
        result_dict["ddnnf_exist_nodecount_plus"] = nb_plus
        result_dict["ddnnf_exist_nodecount_mult"] = nb_times

        # smoothing simple existential quantification of tseitin variables
        sddnnfp = smooth_ddnnf(ddnnfp)
        del ddnnfp
        nb_plus, nb_times = _compute_nb_operations(sddnnfp, include_unused_vars=True)
        print(f"\tSmoothing after simple existential quantification. + ({nb_plus}) * ({nb_times})")
        del sddnnfp
        result_dict["sddnnf_exist_nodecount_plus"] = nb_plus
        result_dict["sddnnf_exist_nodecount_mult"] = nb_times

        # tseitin-artifact removal + existential quantification
        start_time = time.time()
        ddnnft = existential_quantification_tseitin(ddnnf, var_info.tseitin_vars)
        del ddnnf
        end_time = time.time()
        nb_plus, nb_times = _compute_nb_operations(ddnnft)
        print(
            f"\tExistential quantification witth Tseitin took {(end_time - start_time):.3f}s. + ({nb_plus}) * ({nb_times})")
        result_dict["ddnnf_tseitin_nodecount_plus"] = nb_plus
        result_dict["ddnnf_tseitin_nodecount_mult"] = nb_times

        # smooth tseitin ddnnf
        sddnnft = smooth_ddnnf(ddnnft)
        del ddnnft
        nb_plus, nb_times = _compute_nb_operations(sddnnft, include_unused_vars=True)
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


def execute_experiment(result_csv_path):
    _generate_result_csv(result_csv_path)

    for i in range(2, 101):
        model = PrologString(_generate_noisy_or_str_instance(nb_parents=i))
        instance_name = f"noisy_or_{i}"
        _execute_noisy_or(result_csv_path, model, instance_name)


if __name__ == "__main__":
    result_path = "./results/noisy_or.csv"
    execute_experiment(result_path)

