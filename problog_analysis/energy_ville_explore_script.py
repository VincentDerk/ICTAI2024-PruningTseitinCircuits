import os
import subprocess
import sys
import time

from problog.constraint import TrueConstraint
from problog.logic import Term
from problog.program import PrologString
from problog.formula import LogicDAG
from problog.engine import DefaultEngine

from cnf_analysis.cnf_exp_script import compute_nb_operations
from core.cnf2ddnnf import cnf_to_ddnnf
from core.ddnnf import DDNNF
from core.ddnnf_extra import compress_ddnnf, smooth_ddnnf, existential_quantification, \
    existential_quantification_tseitin
from core.varinfo import VariableSetInfo
from problog_analysis.problog2ddnnf import logicdag_to_cnf


def _compile_instance(model: PrologString, timeout, add_query=True) -> (DDNNF, int, VariableSetInfo, str):
    """ returns d-DNNF, compile time, var_info and status """
    ddnnf = None
    compile_time = 0
    var_info = None
    try:
        ddnnf, compile_time, var_info = _energyville_nodel_to_ddnnf(model, add_query=add_query, timeout=timeout)
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


def _energyville_nodel_to_ddnnf(model, timeout, add_query=True) -> (DDNNF, int, VariableSetInfo):
    """
    :param model: ProbLog model containing one query, and no evidence.
    :param timeout:
    :oaram add_query: Whether to add the query as constraint.
    Relevant exceptions are subprocess.CalledProcessError, subprocess.TimeoutExpired, MemoryError
    :return: The DDNNF, compilation time, and Variable info.
    """
    engine = DefaultEngine(label_all=True)
    db = engine.prepare(model)
#    queries = engine.query(db, Term("query", None))
#    evidence = engine.query(db, Term("evidence", None, None))
#    print("Queries:", ", ".join([str(q[0]) for q in queries]))
#    print("Evidence:", ", ".join(["%s=%s" % ev for ev in evidence]))
    gp = engine.ground_all(db)
    gp = LogicDAG.createFrom(gp)  # type: LogicDAG
    # turn evidence-constraints into constraints
    gp.add_constraint(TrueConstraint(gp._names["query"].pop(Term("singly_connected"))))
    gp.add_constraint(TrueConstraint(-gp._names["query"].pop(Term("same_feeder_dissimilar"))))
    gp.add_constraint(TrueConstraint(-gp._names["query"].pop(Term("diff_feeder_similar"))))
    cnf, var_info = logicdag_to_cnf(gp, add_query=add_query)
#    print_cnf(cnf)
#    print(var_info)
    ddnnf, compile_time = cnf_to_ddnnf(cnf, timeout=timeout)
    return ddnnf, compile_time, var_info


def _generate_str_instance():
    instance_str = """
    house(a).
house(b).
house(c).
house(d).

feeder(1).
feeder(2).

0.5 :: connected(X,Y) :- house(X), feeder(Y).

0.8::similar(a,b).
0.8::similar(a,c).
0.8::similar(b,c).

0.2::similar(a,d).
0.2::similar(b,d).
0.2::similar(c,d).

similar(X,Y) :- similar(Y,X).

0.8::map(X,Y) :- connected(X,Y).
0.2::map(X,Y) :- \+connected(X,Y).

unconnected :- house(X), \+connected(X,_).
doubly_connected :- connected(X,Y), connected(X,Z), Y \== Z.
singly_connected :- \+unconnected, \+doubly_connected.

0.5 :: should_same_feeder_be_similar.
1.0 :: should_diff_feeder_be_dissimilar.

same_feeder_dissimilar :-should_same_feeder_be_similar, connected(X,Z), connected(Y,Z), X \==Y, \+similar(X,Y).
diff_feeder_similar :- should_diff_feeder_be_dissimilar, connected(X,Z1), connected(Y,Z2), X \==Y, Z1 \== Z2, similar(X,Y).

evidence(map(a,1)). evidence(map(a,2), false).
evidence(map(b,1)). evidence(map(b,2), false).
evidence(map(c,2)). evidence(map(c,1), false).
evidence(map(d,2)). evidence(map(d,1), false).

query(singly_connected).
query(same_feeder_dissimilar).
query(diff_feeder_similar).

query(connected(X,Y)).
    """
    return instance_str


def _execute_energy_instance(result_csv_path, model, instance_name):
    result_dict = dict()
    result_dict["instance_name"] = instance_name

    print(f"Compiling instance {instance_name}")
    ddnnf, compile_time, var_info, status = _compile_instance(model, add_query=False, timeout=600)
    result_dict["compile_time"] = compile_time
    result_dict["var_count"] = ddnnf.var_count if ddnnf is not None else 0
    result_dict["tseitin_var_count"] = len(var_info.tseitin_vars) if var_info is not None else 0
    print(f"\tCompiled {instance_name} with {status} and compile time {compile_time:.3f}s.")

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
        assert False
        #_write_to_result_csv(result_csv_path, result_dict)
    # else: we printed the error and should look into this instance.


def execute_experiment(result_csv_path):
    model = PrologString(_generate_str_instance())
    instance_name = f"energyville1"
    _execute_energy_instance(result_csv_path, model, instance_name)


if __name__ == "__main__":
    result_path = "./results/energyville1.csv"
    execute_experiment(result_path)

