import pickle

from core.cnf2ddnnf import _load_nnf
from core.ddnnf import DDNNF


def convert_nnf(filename: str, output_filename: str):
    ddnnf = _load_nnf(filename)

    # save files
    output_filename_ddnnf = output_filename + "_ddnnf.pickle"
    with open(output_filename_ddnnf, "wb") as f:
        pickle.dump(ddnnf, f)


if __name__ == "__main__":
    import argparse

    argparser = argparse.ArgumentParser()
    argparser.add_argument("filename")
    argparser.add_argument("output_filename")
    args = argparser.parse_args()

    convert_nnf(**vars(args))


