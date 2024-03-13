import resource
import time

from cnf_analysis.cnf_exp_script import _compute_nb_operations, _compile_instance, _get_varinfo
from core.cnf import read_cnf
from core.ddnnf_extra import compress_ddnnf, smooth_ddnnf, existential_quantification_tseitin, \
    existential_quantification


def execute_experiment(instance_filepath, timeout=600):
    MAX_VMEMORY = 4 * 1024 * 1024 * 1024  # 4GB (in bytes)
    resource.setrlimit(resource.RLIMIT_AS, (MAX_VMEMORY, resource.RLIM_INFINITY))

    #   get_cnf_info
    cnf = read_cnf(instance_filepath)
    var_count = cnf.var_count
    clause_count = len(cnf.clauses)
    print(f"Handling {instance_filepath}; vars={var_count}; clauses={clause_count}")

    #   extract varinfo from instance
    var_info = _get_varinfo(cnf)
    del cnf

    #   compile instance to ddnnf
    ddnnf, compile_time, status = _compile_instance(instance_filepath, timeout=timeout)
    print(f"\tCompiled {instance_filepath} with {status} and compile time {compile_time:.3f}s.")

    if ddnnf is not None and status == "success":
        # compress d-DNNF
        ddnnf = compress_ddnnf(ddnnf)

        # ddnnf_nodecount
        nb_plus, nb_times = _compute_nb_operations(ddnnf)
        print(f"\td-DNNF after compression. + ({nb_plus}) * ({nb_times})")

        # sddnnf_nodecount
        start_time = time.time()
        sddnnf = smooth_ddnnf(ddnnf)
        end_time = time.time()
        nb_plus, nb_times = _compute_nb_operations(sddnnf, include_unused_vars=True)
        print(f"\tSmoothing took {(end_time - start_time):.3f}s. + ({nb_plus}) * ({nb_times})")
        del sddnnf

        # simple existential quantification of tseitin variables
        start_time = time.time()
        ddnnfp = existential_quantification(ddnnf, var_info.tseitin_vars)
        # print(f"before {len(ddnnfp)} and {len(ddnnfp.unused_vars)}")
        # ddnnfp = compress_ddnnf(ddnnfp)
        # print(f"after {len(ddnnfp)} and {len(ddnnfp.unused_vars)}")
        end_time = time.time()
        nb_plus, nb_times = _compute_nb_operations(ddnnfp)
        print(
            f"\tExistential quantification took {(end_time - start_time):.3f}s. + ({nb_plus}) * ({nb_times})")

        # smoothing simple existential quantification of tseitin variables
        sddnnfp = smooth_ddnnf(ddnnfp)
        del ddnnfp
        nb_plus, nb_times = _compute_nb_operations(sddnnfp, include_unused_vars=True)
        print(f"\tSmoothing after simple existential quantification. + ({nb_plus}) * ({nb_times})")
        del sddnnfp

        # tseitin-artifact removal + existential quantification
        start_time = time.time()
        ddnnft = existential_quantification_tseitin(ddnnf, var_info.tseitin_vars)
        del ddnnf
        end_time = time.time()
        nb_plus, nb_times = _compute_nb_operations(ddnnft)
        print(
            f"\tExistential quantification witth Tseitin took {(end_time - start_time):.3f}s. + ({nb_plus}) * ({nb_times})")

        # smooth tseitin ddnnf
        sddnnft = smooth_ddnnf(ddnnft)
        del ddnnft
        nb_plus, nb_times = _compute_nb_operations(sddnnft, include_unused_vars=True)
        del sddnnft
        print(f"\tSmooth after Tseitin. + ({nb_plus}) * ({nb_times})")


if __name__ == "__main__":
    # cnf_instances_csv = "results/test-cnfs.csv"
    cnf_instance_path = "../sources/cnf2tseitin/cnf/MC2023_track1-mc_public/mc2023_track1_037.cnf"
    execute_experiment(cnf_instance_path, timeout=600)

