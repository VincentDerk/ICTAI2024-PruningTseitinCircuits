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


def _scatter_reg_vs_tseitin(result_objs: List[_ResultObj], img_filepath):
    data_x = [r.ddnnf_nodecount for r in result_objs]
    data_x = np.array(data_x)
    xlabel = "number of nodes in d-DNNF"
    data_y = [r.ddnnft_nodecount / r.ddnnf_nodecount * 100 for r in result_objs]
    data_y = np.array(data_y)
    ylabel = "nodes remaining in d-DNNF+t (\%)"

    # results
    avg = np.average(100 - data_y)  # avg % nodes removed
    median = np.median(100 - data_y)  # median % nodes removed
    std = np.std(100 - data_y)  # std % nodes removed
    nb_improved = np.sum(data_y < 100)
    print(f"Number of nodes removed (%). Average={avg:.3f}%\tMedian={median:.3f}%\tstd={std:.3f}%)")
    print(f"nb of improved instances: {nb_improved}/{len(data_y)}")

    # scatter
    logscale = True
    plt.style.use("../tex.mplstyle")
    fig, ax = plt.subplots()  # nrows=1, ncols=1, figsize=figsize)
    fig.set_figwidth(3.31)
    fig.set_figheight(3)
    ax.set_ylim([0, 100])
    ax.scatter(data_x, data_y, color="red", alpha=0.4, zorder=5, marker=".")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, color='black', ls=':', lw=1, zorder=1)
    ax.set_xscale('log')

    # setting ticks font properties
    # ax.set_xticklabels(ax.get_xticks(), self.f_props)
    # ax.set_yticklabels(ax.get_yticks(), self.f_props)

    # formatter
    strFormatter = plt.FormatStrFormatter('%d')
    logFormatter = plt.LogFormatterMathtext(base=10)
    ax.xaxis.set_major_formatter(strFormatter if not logscale else logFormatter)

    # setting frame thickness
    for i in ax.spines.values():
        i.set_linewidth(1)

    plt.savefig(img_filepath, bbox_inches='tight')
    # plt.show()


def _scatter_prop_vs_tseitin(result_objs: List[_ResultObj], img_filepath):
    data_x = [r.ddnnfp_nodecount for r in result_objs]
    data_x = np.array(data_x)
    xlabel = "number of nodes in d-DNNF+p"
    data_y = [r.ddnnft_nodecount / r.ddnnfp_nodecount * 100 for r in result_objs]
    data_y = np.array(data_y)
    ylabel = "nodes remaining in d-DNNF+t (\%)"

    # results
    nb_improved = np.sum(data_y < 100)
    nb_same = np.sum(data_y == 100)
    nb_worse = np.sum(data_y > 100)
    avg_improvement = np.average(100 - data_y[data_y < 100])
    median_improvement = np.median(100 - data_y[data_y < 100])
    std_improvement = np.std(100 - data_y[data_y < 100])
    # avg_worse = np.average(data_y[data_y > 100] - 100)
    # median_worse = np.median(data_y[data_y > 100] - 100)
    # std_worse = np.std(data_y[data_y > 100] - 100)
    print(f"{len(data_y)} instances:")
    print(f"\tnb improved: {nb_improved};"
          f"\tremoved avg={avg_improvement:.3f}%"
          f"\tmedian={median_improvement:.3f}%"
          f"\tstd={std_improvement:.3f}%")
    print(f"\tnb same: {nb_same}")
    print(f"\tnb_worse: {nb_worse};")
    #       f"\tincreased avg={avg_worse:.3f}%"
    #       f"\tmedian={median_worse:.3f}%"
    #       f"std={std_worse:.3f}%")

    # plot
    logscale = True
    plt.style.use("../tex.mplstyle")
    fig, ax = plt.subplots()  # nrows=1, ncols=1, figsize=figsize)
    fig.set_figwidth(3.31)
    fig.set_figheight(3)

    # scatter
    ax.scatter(data_x, data_y, color="red", alpha=0.4, zorder=5, marker=".")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, color='black', ls=':', lw=1, zorder=1)
    ax.set_xscale('log')
    ax.set_ylim([0, 100])

    # setting ticks font properties
    # ax.set_xticklabels(ax.get_xticks(), self.f_props)
    # ax.set_yticklabels(ax.get_yticks(), self.f_props)

    # formatter
    strFormatter = plt.FormatStrFormatter('%d')
    logFormatter = plt.LogFormatterMathtext(base=10)
    ax.xaxis.set_major_formatter(strFormatter if not logscale else logFormatter)

    # setting frame thickness
    for i in ax.spines.values():
        i.set_linewidth(1)

    plt.savefig(img_filepath, bbox_inches='tight')
    # plt.show()


if __name__ == "__main__":
    result_csv = "./results/problog_exp.csv"
    results = read_from_file(result_csv)
    print(f"{len(results)} instances")
    print("instance".ljust(90) + "\t|ddnnf|\t|ddnnf+p| (remaining)\t|ddnn+t| (remaining)")
    for result in results:
        rel_compression = result.ddnnfp_nodecount / result.ddnnf_nodecount
        rel_compression2 = result.ddnnft_nodecount / result.ddnnf_nodecount
        msg = (f"{result.instance_name}".ljust(90) + f"\t{result.ddnnf_nodecount}\t" +
               f"\t{result.ddnnfp_nodecount}({rel_compression:.2f})" +
               f"\t{result.ddnnft_nodecount} ({rel_compression2:.2f})")
        print(msg)
    print("----------------")
    print("reg vs tseitin")
    _scatter_reg_vs_tseitin(results, "./results/problog_exp_reg_vs_tseitin.pdf")
    print("")
    print("prop vs tseitin")
    _scatter_prop_vs_tseitin(results, "./results/problog_exp_prop_vs_tseitin.pdf")
