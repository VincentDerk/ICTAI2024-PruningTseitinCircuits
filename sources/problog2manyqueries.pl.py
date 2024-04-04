"""
    A script to convert a ground ProbLog file (e.g. a BN in ProbLog) to a .pl file containing
    every possible query of that file.
"""
import string
import shutil
from typing import Set

from problog.clausedb import ClauseDB
from problog.logic import Clause, AnnotatedDisjunction, Term
from problog.program import PrologFile
from problog.engine import DefaultEngine


def _pl_to_many(filepath_in, filename_out):
    """ output_path is a path and filename """
    model = PrologFile(filepath_in)
    engine = DefaultEngine(label_all=True)
    db = engine.prepare(model)

    derived_atoms = extract_ground_derived_atoms(db)
    print(f"Found {len(derived_atoms)} unique ground atoms.")
    # for atom in derived_atoms:
    #     print(atom)

    from pathlib import Path
    file = Path(filename_out)
    file.parent.mkdir(parents=True, exist_ok=True)
    used_filenames = set()
    # for each atom we create a weighted CNF:
    for atom in derived_atoms:
        # fix atom str representation to filename
        atom_repr = _sanitize_filename(str(atom))
        # resolve filename conflicts
        if atom_repr in used_filenames:
            i = 1
            while atom_repr + str(i) in used_filenames:
                i += 1
            atom_repr = atom_repr + str(i)
        used_filenames.add(atom_repr)
        # create new pl file
        filepath_out = filename_out + f"{atom_repr}.pl"
        shutil.copyfile(filepath_in, filepath_out)
        with open(filepath_out, "a") as f:
            f.write(f"\nquery({atom}).")


def _sanitize_filename(filename_string):
    legal_characters = "-_.() %s%s" % (string.ascii_letters, string.digits)
    # Replace all illegal characters.
    sanitized_filename = ''.join(c for c in filename_string if c in legal_characters)
    return sanitized_filename


def extract_ground_derived_atoms(db: ClauseDB) -> Set[Term]:
    """ Extract all ground derived atoms from the ground program. """
    derived_atoms = set()
    for node in db:
        if type(node) == Clause:
            # note: ignore predicates beginning with body_, or with _
            if node.head.functor.startswith("body_") or node.head.functor.startswith("_"):
                continue
            derived_atoms.add(node.head)
        if type(node) == AnnotatedDisjunction:
            for term in node.heads:
                derived_atoms.add(term.with_probability())
    return derived_atoms


def main():
    src_filepath = "./problog_bn_src/alarm.net.pl"
    output_filepath = "./problog_bn_query/alarm.net."
    _pl_to_many(src_filepath, output_filepath)


if __name__ == "__main__":
    main()
