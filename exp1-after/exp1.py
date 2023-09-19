import pickle

from core.ddnnf import ddnnf_to_dot
from detafter.postdetector import get_tseitin_artifacts
from graphviz import Source


def main(filename_ddnnf, filename_tseitin):
    with open(filename_ddnnf, "rb") as f:
        ddnnf = pickle.load(f)  # type: DDNNF
    with open(filename_tseitin, "rb") as f:
        tseitin_vars = pickle.load(f)  # type: List[int]

    artifacts, overlay_vars = get_tseitin_artifacts(ddnnf, tseitin_vars)  # type: FormulaOverlayList
    print(artifacts)
    print(tseitin_vars)

    # TODO: remove smoothing nodes from artifacts: track whether there is at least one tseitin var under a node.

    def _color_artifact(index, node):
        if artifacts[index]:
            return 'fillcolor="red"'
        else:
            return 'fillcolor="white"'
    Source(ddnnf_to_dot(ddnnf, _color_artifact)).render(view=True)
    # Source(to_dot(nnf, not_as_node=False)).render(dotprefix + "nnf", view=False)


if __name__ == "__main__":
    import argparse
    argparser = argparse.ArgumentParser()
    argparser.add_argument("filename_ddnnf")
    argparser.add_argument("filename_tseitin")
    args = argparser.parse_args()

    main(**vars(args))
