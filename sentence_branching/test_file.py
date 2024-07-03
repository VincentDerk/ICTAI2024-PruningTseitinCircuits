import time

from pysdd import sdd
from pysdd.sdd import SddManager, Fnf, Vtree, CompilerOptions, SddNode

if __name__ == "__main__":
    test_cnf_path = b"../sources/cnf2tseitin/cnf/MC2022_track2-wmc_public/mc2022_track2_007.cnf"
    options = CompilerOptions(
                              minimize_cardinality=True,
                              vtree_search_mode=-1,
                              verbose=True,
                                post_search=True)
    # test_cnf_path = b"../sources/cnf2tseitin/cnf/MC2023_track2-wmc_public/mc2023_mc2023_track2_023.cnf"
    fnf = Fnf.from_cnf_file(test_cnf_path)
    vtree = Vtree(var_count=fnf.var_count, vtree_type="balanced")
    manager = SddManager.from_vtree(vtree)
    manager.set_options(options)
    print("compiling...")
    c1 = time.time()
    # node = manager.from_cnf_file(test_cnf_path)
    node = manager.fnf_to_sdd(fnf)  # type: SddNode
    c2 = time.time()
    secs = c2 - c1
    print("")
    print(f"compilation time         : {secs:.3f} sec")

    print(node.size())

