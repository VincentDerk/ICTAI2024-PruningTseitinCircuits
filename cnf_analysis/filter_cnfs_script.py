import os
import pickle

from tqdm import tqdm

from core.cnf import read_cnf
from core.varinfo import VariableSetInfo
from cnf_analysis.cnf2tseitin import determine_tseitin_from_cnf
from sources.cnf2tseitin.config import model_counting_folders


def analyse_cnf_folder(output_filepath):
    folder_dirs = model_counting_folders.copy()

    with open(output_filepath, "w") as f:
        f.write("filename_cnf,clause_count,var_count,tseitin_var_count\n")
        for folder_dir in tqdm(folder_dirs):
            # go over all files in folder_dir
            for filename in tqdm(os.listdir(folder_dir)):
                if filename.endswith(".cnf"):
                    filename_cnf = os.path.join(folder_dir, filename)
                    print(f"File: {filename_cnf}")
                    cnf = read_cnf(filename_cnf)
                    var_count = cnf.var_count
                    clause_count = cnf.clause_count()
                    tseitin_var_count = len(determine_tseitin_from_cnf(cnf))
                    print(f"\tFound {tseitin_var_count} Tseitin vars out of {var_count} ({tseitin_var_count/var_count*100:.2f}%).")
                    f.write(f"{filename_cnf},{clause_count},{var_count},{tseitin_var_count}\n")


def filter_cnf_instances(input_filepath, output_filepath, separator=","):
    total_inst_count = 0
    kept_inst_count = 0
    copied_header = False
    with open(input_filepath, "r") as fin, open(output_filepath, "w") as fout:
        for line in fin.readlines():
            # header
            if not copied_header:
                assert line == "filename_cnf,clause_count,var_count,tseitin_var_count\n"
                fout.write(line)
                copied_header = True
                continue

            # entries
            line = line.split(separator)
            assert len(line) == 4
            total_inst_count += 1
            filename_cnf = line[0]
            clause_count = int(line[1])
            var_count = int(line[2])
            tseitin_var_count = int(line[3])
            rel_tseitin_count = tseitin_var_count / var_count
            if rel_tseitin_count > 0.25:
                kept_inst_count += 1
                fout.write(f"{filename_cnf},{clause_count},{var_count},{tseitin_var_count}\n")
    print(f"Filtered CNF instances from {input_filepath}")
    print(f"{kept_inst_count} / {total_inst_count} remaining in {output_filepath}")


def create_varinfo_per_instance(input_filepath, separator=","):
    with open(input_filepath, "r") as f:
        for line in f.readlines()[1:]:
            line = line.split(separator)
            instance_path = line[0]

            # determine varinfo
            cnf = read_cnf(instance_path)
            tseitin_vars = determine_tseitin_from_cnf(cnf)
            var_info = VariableSetInfo(tseitin_vars=tseitin_vars)
            assert len(tseitin_vars) > 0, "No tseitin variables detected, why create this?"

            # store varinfo to file
            parent_folder_name = os.path.basename(os.path.dirname(instance_path))
            output_filedir = os.path.join("../sources/ddnnf/", parent_folder_name)
            os.makedirs(output_filedir, exist_ok=True)
            new_filename = os.path.basename(instance_path)[:-4] + "_varinfo.pickle"
            output_filepath = os.path.join(output_filedir, new_filename)
            with open(output_filepath, "wb") as f:
                pickle.dump(var_info, f)
            print(f"Stored varinfo from {instance_path} to {output_filepath}")


if __name__ == "__main__":
    # # step 1 - extract potential Tseitin variables
    out_filepath = "results/tseitin-var-counts-mcc.csv"
    # analyse_cnf_folder(output_filepath=out_filepath)
    # # step 2 - extract and store .varinfo only for certain instances
    filtered_out_filepath = "results/tseitin-var-counts-mcc-filtered.csv"
    filter_cnf_instances(input_filepath=out_filepath, output_filepath=filtered_out_filepath)


    # ddnnf = compile_wmc_instance(
    #     filename_cnf="cnf/test_d4_small.cnf",
    #     # filename_cnf="cnf/MC2023_track2-wmc_private/mc2023_mc2023_track2_012.cnf",
    #     filename_output="./test-d4",
    #     nnf=True)

    # print(ddnnf)
    # mc = compute_model_count(ddnnf)
    # print(mc)
    # Source(ddnnf_to_dot(ddnnf)).render(view=True)

    # import argparse
    # argparser = argparse.ArgumentParser()
    # argparser.add_argument("filename_cnf")
    # argparser.add_argument("filename_output")
    # argparser.add_argument("--nnf", action="store_true")
    # argparser.set_defaults(nnf=False)
    # args = argparser.parse_args()
    #