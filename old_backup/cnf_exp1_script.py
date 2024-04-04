import os
import pickle
import random
import subprocess
import sys

from tqdm import tqdm

script_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(os.path.dirname(script_dir))

# Add the parent directory to sys.path
sys.path.append(parent_dir)

from core.cnf import read_cnf
from core.cnf2ddnnf import cnf_to_ddnnf
from core.ddnnf import ddnnf_to_dot, DDNNF
from core.ddnnf_evaluator import compute_model_count
from core.varinfo import VariableSetInfo
from sources.cnf2tseitin.config import model_counting_folders


def _compile_and_save_instance(input_filepath: str, output_filepath: str, timeout):
    cnf = read_cnf(input_filepath)
    try:
        ddnnf = cnf_to_ddnnf(cnf, timeout=timeout)

        # save files
        with open(output_filepath, "wb") as f:
            pickle.dump(ddnnf, f)
    except subprocess.CalledProcessError as err:
        print(err, file=sys.stderr)
        ddnnf = None
    except subprocess.TimeoutExpired as err:
        print(f"Timeout error when compiling {input_filepath}. Skipped it.")
        with open(output_filepath, "wb") as f:
            pickle.dump(DDNNF(), f)
        ddnnf = None
    return ddnnf


def _load_instance_list(csv_filepath):
    instances = list()
    with open(csv_filepath, "r") as f:
        for line in f.readlines()[1:]:
            line = line.split(",")
            instance_path = line[0]
            instances.append(instance_path)
    return instances


def compile_instances(instances_csv_filepath, timeout=600):
    """ compiled_csv_filepath includes files that have been attempted at before. """
    instances = _load_instance_list(instances_csv_filepath)
    for instance_path in tqdm(instances):
        # extract directory
        parent_folder_name = os.path.basename(os.path.dirname(instance_path))
        output_filedir = os.path.join("../sources/ddnnf/", parent_folder_name)
        os.makedirs(output_filedir, exist_ok=True)
        new_filename = os.path.basename(instance_path)[:-4] + "_ddnnf.pickle"
        output_filepath = os.path.join(output_filedir, new_filename)
        # compile
        if not os.path.exists(output_filepath):
            print(f"\tCompiling {instance_path} into {output_filepath}")
            _compile_and_save_instance(instance_path, output_filepath, timeout=timeout)
        else:
            print(f"{output_filepath} already existed. Skipped compiling it.")

    # folder_dirs = model_counting_folders.copy()
    # for folder_dir in tqdm(folder_dirs):
    #     parent_folder_name = os.path.basename(os.path.dirname(folder_dir))
    #     output_filedir = os.path.join("../ddnnf/", parent_folder_name)
    #     os.makedirs(output_filedir, exist_ok=True)
    #
    #     # go over all files in folder_dir
    #     filenames = os.listdir(folder_dir)
    #     random.shuffle(filenames)
    #     for filename in tqdm(os.listdir(folder_dir)):
    #         if filename.endswith(".cnf"):
    #             filepath = os.path.join(folder_dir, filename)
    #             new_filename = filename[:-4] + "_ddnnf.pickle"
    #             output_filepath = os.path.join(output_filedir, new_filename)
    #             if not os.path.exists(output_filepath):
    #                 print(f"\tCompiling {filepath} into {output_filepath}")
    #                 _compile_and_save_instance(filepath, output_filepath)
    #             else:
    #                 print(f"{output_filepath} already existed. Skipped compiling it.")


if __name__ == "__main__":
    cnf_instances_csv = "./tseitin-var-counts-mcc-filtered.csv"
    compile_results_csv = "./tseitin-var-counts-mcc-filtered-compiled.csv"
    compile_instances(cnf_instances_csv,
                      timeout=600)
