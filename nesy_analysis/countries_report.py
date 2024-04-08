from typing import List

import matplotlib.pyplot as plt
import numpy as np


class _ResultObj:

    def __init__(self, instance_name):
        self.instance_name = instance_name
        self.var_count = 0
        self.tseitin_var_count = 0
        self.compile_time = None

        self.ddnnf_nodecount = 0
        self.ddnnfp_nodecount = 0
        self.ddnnft_nodecount = 0

        self.sddnnf_nodecount = 0
        self.sddnnfp_nodecount = 0
        self.sddnnft_nodecount = 0


def read_from_file(csv_result_filepath: str):

    with open(csv_result_filepath, "r") as f:
        lines = f.readlines()
    result_objs = []
    nb_timeouts = 0
    nb_mems = 0
    for line in lines[1:]:
        line = line.strip()
        if line == "":
            continue
        parts = line.split(",")
        assert len(parts) == 16, f"Error: {line}; with length {len(parts)}"
        instance_name = parts[0]
        result_obj = _ResultObj(instance_name)
        result_obj.var_count = int(parts[1])
        result_obj.tseitin_var_count = int(parts[2])
        result_obj.compile_time = float(parts[3])
        # timestamp = 5
        if parts[6] == "MEM_ERR":
            nb_mems += 1
            continue

        if parts[6] == "TO":
            nb_timeouts += 1
            continue

        result_obj.ddnnf_nodecount = int(parts[4]) + int(parts[5])
        result_obj.sddnnf_nodecount = int(parts[6]) + int(parts[7])
        result_obj.ddnnfp_nodecount = int(parts[8]) + int(parts[9])
        result_obj.sddnnfp_nodecount = int(parts[10]) + int(parts[11])
        result_obj.ddnnft_nodecount = int(parts[12]) + int(parts[13])
        result_obj.sddnnft_nodecount = int(parts[14]) + int(parts[15])

        result_objs.append(result_obj)
    print(f"nb_timeouts={nb_timeouts}; nb_mems={nb_mems}")
    return result_objs


if __name__ == "__main__":
    result_csv = "./results/countries_exp.csv"
    results = read_from_file(result_csv)
    print(f"{len(results)} instances")
    print("instance".ljust(90) + "\t|ddnnf|\t|ddnnf+p| (remaining)\t|ddnn+t| (remaining)")
    for result in results:
        rel_compression = result.ddnnfp_nodecount / result.ddnnf_nodecount
        rel_compression2 = result.ddnnft_nodecount / result.ddnnf_nodecount
        msg = (f"{result.instance_name}".ljust(90) + f"\t{result.ddnnf_nodecount}\t" +
               f"\t{result.ddnnfp_nodecount} ({rel_compression:.2f})" +
               f"\t{result.ddnnft_nodecount} ({rel_compression2:.2f})")
        print(msg)
