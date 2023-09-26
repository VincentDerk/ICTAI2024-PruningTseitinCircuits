import pickle

from core.ddnnf import ddnnf_to_dot
from detafter.postdetector import get_tseitin_artifacts, get_artifact_size
from graphviz import Source


def main(filename_ddnnf, filename_varinfo):
    with open(filename_ddnnf, "rb") as f:
        ddnnf = pickle.load(f)  # type: DDNNF
    with open(filename_varinfo, "rb") as f:
        var_info = pickle.load(f)  # type: VariableSetInfo

    tseitin_vars = var_info.tseitin_vars
    artifacts = get_tseitin_artifacts(ddnnf, tseitin_vars)  # type: FormulaOverlayList
    num_saved, num_removed, num_added = get_artifact_size(ddnnf, artifacts, tseitin_vars)
    num_nodes = len(ddnnf)
    print(f"Num nodes removed: {num_removed}.")
    print(f"Num nodes added: {num_added}.")
    print(f"Num nodes fewer: {num_saved}.")
    print(f"Out of {num_nodes} ({(num_saved / num_nodes * 100):.2f}%) (incl. vars).")
    print(f"Out of {num_nodes - ddnnf.var_count} ({(num_saved / (num_nodes - ddnnf.var_count)*100):.2f}%) (excl. vars)")
    print(tseitin_vars)
    artifact_to_dot(ddnnf, artifacts, tseitin_vars, display=True)



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
    argparser.add_argument("filename_ddnnf")
    argparser.add_argument("filename_varinfo")
    args = argparser.parse_args()

    main(**vars(args))
