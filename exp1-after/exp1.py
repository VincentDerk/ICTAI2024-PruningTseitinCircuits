import glob
import pickle

from core.ddnnf import ddnnf_to_dot
from detafter.postdetector import get_tseitin_artifacts, get_artifact_size
from graphviz import Source


def main():
    datasets = glob.glob("../sources/ddnnf/*_ddnnf.pickle")

    for instance in datasets:
        filename_ddnnf = instance
        filename_varinfo = filename_ddnnf[:-len("_ddnnf.pickle")] + "_varinfo.pickle"
        print(f"----- {filename_ddnnf} -----")
        stats_instance = _get_stats_of_instance(filename_ddnnf, filename_varinfo)
        num_saved, num_removed, num_added, num_total_nodes, var_count = stats_instance
        #
        print(f"Num nodes fewer: {num_saved} = -{num_removed} (del) + {num_added} (add)")
        rel_saved_total = num_saved / num_total_nodes
        rel_saved_novar = num_saved / (num_total_nodes - var_count)
        print(f"Out of {num_total_nodes} ({(rel_saved_total * 100):.2f}%) (incl. vars).")
        print(f"Out of {num_total_nodes - var_count} ({(rel_saved_novar*100):.2f}%) (excl. vars)")


def _get_stats_of_instance(filename_ddnnf, filename_varinfo):
    """

    :param filename_ddnnf:
    :param filename_varinfo:
    :return: A tuple of 4 elements.
        1. The number of nodes that artifact replacement would save.
            (equal to third minus second returned value)
        2. The number of nodes that artifacts would remove.
        3. The number of nodes that artifact replacement would add (number of new smooth nodes)
        4. The total number of nodes currently in the ddnnf (includes variable nodes)
        5. The number of variables in the ddnnf.
    """
    with open(filename_ddnnf, "rb") as f:
        ddnnf = pickle.load(f)  # type: DDNNF
    with open(filename_varinfo, "rb") as f:
        var_info = pickle.load(f)  # type: VariableSetInfo

    tseitin_vars = var_info.tseitin_vars
    artifacts = get_tseitin_artifacts(ddnnf, tseitin_vars)  # type: FormulaOverlayList
    num_saved, num_removed, num_added = get_artifact_size(ddnnf, artifacts, tseitin_vars)
    num_total_nodes = len(ddnnf)
    return num_saved, num_removed, num_added, num_total_nodes, ddnnf.var_count


def artifact_to_dot(ddnnf, artifacts, tseitin_vars, display=True):

    def _color_artifact(index, node):
        if artifacts[index]:
            return 'fillcolor="red"'
        elif node.node_type == "atom" and index in tseitin_vars:
            return 'fillcolor="green"'
        else:
            return 'fillcolor="white"'
    # print(ddnnf_to_dot(ddnnf, _color_artifact))
    Source(ddnnf_to_dot(ddnnf, _color_artifact)).render(view=display)


if __name__ == "__main__":
    import argparse
    argparser = argparse.ArgumentParser()
    args = argparser.parse_args()

    main(**vars(args))
