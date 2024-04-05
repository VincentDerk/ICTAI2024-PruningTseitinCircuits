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


def visualize_results(img_filepath, result_objs: List[_ResultObj]):
    data_x = np.array(range(len(result_objs)))
    data_yp = [r.ddnnfp_nodecount / r.ddnnf_nodecount *100 for r in result_objs]
    data_yt = [r.ddnnft_nodecount / r.ddnnf_nodecount *100 for r in result_objs]

    def _extract_name(name):
        return name.split("/")[-1].replace(".pl", "")
    tick_labels = [_extract_name(r.instance_name) for r in result_objs]
    fig, ax = plt.subplots()  # nrows=1, ncols=1, figsize=figsize)
    plt.bar(data_x - 0.2, height=data_yp, width=0.4, color='blue', label="d-DNNF+p", hatch="//")
    plt.bar(data_x + 0.2,  height=data_yt, width=0.4, color='green', label="d-DNNF+t")
    plt.xticks(data_x, tick_labels, y=-0.05)

    for i, label in enumerate(ax.get_xticklabels()):
        if i % 2:
            label.set_va('top')
        else:
            pass
            label.set_va('bottom')

    ax.set_xlabel("BN instance")
    ax.set_ylabel("nodes remaining (%)")
    ax.legend()

    # ax.set_xlim([0, maxval])
    # ax.set_ylim([0, maxval])

    #ax.grid(True, color='black', ls=':', lw=1, zorder=1)

    # setting frame thickness
    # for i in six.itervalues(ax.spines):
    #     i.set_linewidth(1)

    plt.savefig(img_filepath, bbox_inches='tight')
    # Show the plot
    # plt.show()


if __name__ == "__main__":
    result_csv = "./results/bn_no_tseitin_exp.csv"
    results = read_from_file(result_csv)
    for result in results:
        rel_compression = result.ddnnfp_nodecount / result.ddnnf_nodecount
        rel_compression2 = result.ddnnft_nodecount / result.ddnnf_nodecount
        print(f"{result.instance_name}    \t\t{result.ddnnf_nodecount}\t{result.ddnnfp_nodecount} ({rel_compression:.2f})"
              f"\t{result.ddnnft_nodecount} ({rel_compression2:.2f})")
    visualize_results("./results/bn_no_tseitin_exp.pdf", results)
