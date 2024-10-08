from typing import List
import matplotlib.pyplot as plt
import numpy as np


class _ResultObj:

    def __init__(self, cnf_path):
        self.instance_name = cnf_path
        self.clause_count = 0
        self.var_count = 0
        self.tseitin_var_count = 0
        self.compile_time = None

        self.ddnnf_nodecount = 0
        self.ddnnfp_nodecount = 0
        self.ddnnft_nodecount = 0

        self.sddnnf_nodecount = 0
        self.sddnnfp_nodecount = 0
        self.sddnnft_nodecount = 0

    def _signature(self):
        return (self.clause_count, self.var_count,
                self.ddnnf_nodecount, self.ddnnfp_nodecount, self.ddnnft_nodecount)

    def __eq__(self, other):
        """ whether it is likely the same instance """
        if not isinstance(other, _ResultObj):
            return False
        return self._signature() == other._signature()

    def __hash__(self):
        return hash(self._signature())



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
        assert len(parts) == 18, f"Error: {line}; with length {len(parts)}"
        cnf_path = parts[0]
        result_obj = _ResultObj(cnf_path)
        result_obj.clause_count = int(parts[1])
        result_obj.var_count = int(parts[2])
        result_obj.tseitin_var_count = int(parts[3])
        result_obj.compile_time = float(parts[4])
        # timestamp = 5
        if parts[6] == "MEM_ERR":
            nb_mems += 1
            continue

        if parts[6] == "TO":
            nb_timeouts += 1
            continue

        if any((parts[x] == "MEM_ERR2" for x in [6,8,10,12,14,16])):
            nb_mems += 1
            continue

        result_obj.ddnnf_nodecount = int(parts[6]) + int(parts[7])
        result_obj.sddnnf_nodecount = int(parts[8]) + int(parts[9])
        result_obj.ddnnfp_nodecount = int(parts[10]) + int(parts[11])
        result_obj.sddnnfp_nodecount = int(parts[12]) + int(parts[13])
        result_obj.ddnnft_nodecount = int(parts[14]) + int(parts[15])
        result_obj.sddnnft_nodecount = int(parts[16]) + int(parts[17])

        result_objs.append(result_obj)
    print(f"nb_timeouts={nb_timeouts}; nb_mems={nb_mems}")
    return result_objs


def _filter_duplicates(result_objs):
    result_objs = sorted(result_objs, key=lambda x: x._signature())
    result_objs_filtered = []
    for i in range(len(result_objs)):
        if i == 0 or result_objs[i] != result_objs[i-1]:
            result_objs_filtered.append(result_objs[i])
    return result_objs_filtered


def _print_info(result_objs: List[_ResultObj]):
    """ compare existential quantification + simple propagation versus tseitin-artifact removal. """
    data_d = np.array([r.ddnnf_nodecount for r in result_objs])
    data_p = np.array([r.ddnnfp_nodecount for r in result_objs])
    data_t = np.array([r.ddnnft_nodecount for r in result_objs])
    nb_inst = len(data_d)

    print("-- d-DNNF versus d-DNNF+t")
    num_improvements = np.sum(data_t < data_d)
    num_same = np.sum(data_t == data_d)
    print(f"Number of improvements: {num_improvements}/{nb_inst}")
    print(f"Number of same: {num_same}/{nb_inst}")
    print("Overall:")
    rel_pruned = (1 - data_t / data_d) * 100  # avg number of nodes removed
    print(f"\tAvg: {np.average(rel_pruned):.1f}% nodes removed.")
    print(f"\tMedian: {np.median(rel_pruned):.1f}% nodes removed.")
    print(f"\tStd: {np.std(rel_pruned):.1f}% nodes removed.")

    print("\n-- d-DNNF+p versus d-DNNF+t")
    num_improvements = np.sum(data_t < data_p)
    num_same = np.sum(data_t == data_p)
    print(f"Number of improvements: {num_improvements}/{nb_inst}")
    print(f"Number of same: {num_same}/{nb_inst}")
    print("Overall:")
    rel_pruned = (1 - data_t / data_p) * 100  # avg number of nodes removed
    print(f"\tAvg: {np.average(rel_pruned):.1f}% nodes removed.")
    print(f"\tMedian: {np.median(rel_pruned):.1f}% nodes removed.")
    print(f"\tStd: {np.std(rel_pruned):.1f}% nodes removed.")
    print("For those improved:")
    rel_pruned_improved_only = rel_pruned[rel_pruned > 0]
    print(f"\tAvg: {np.average(rel_pruned_improved_only):.1f}% nodes removed.")
    print(f"\tMedian: {np.median(rel_pruned_improved_only):.1f}% nodes removed.")
    print(f"\tStd: {np.std(rel_pruned_improved_only):.1f}% nodes removed.")



def _scatterplot_pt(result_objs: List[_ResultObj]):
    data_x = [r.ddnnfp_nodecount for r in result_objs]
    data_x = np.array(data_x)
    xlabel = "|d-DNNF| w simple existential"
    data_y = [r.ddnnft_nodecount for r in result_objs]
    data_y = np.array(data_y)
    ylabel = "|d-DNNF| w/o tseitin artifacts"


    maxval = max(max(data_x), max(data_y))
    logscale = True
    area_parameter = 10
    plt.style.use("../tex.mplstyle")
    fig, ax = plt.subplots()  # nrows=1, ncols=1, figsize=figsize)
    fig.set_figwidth(3.31)
    fig.set_figheight(2.04)

    step = int(maxval / 10)
    x = np.arange(0, maxval + step, step=step)

    # # "good" area
    plt.plot(x, x, color='black', ls=':', lw=1.5, zorder=3)
    if logscale:
        neg_mult = 1 / area_parameter
        pos_mult = area_parameter
        ax.plot(x, neg_mult * x, 'g:', lw=1.5, zorder=3)
        ax.plot(x, pos_mult * x, 'g:', lw=1.5, zorder=3)
        ax.fill_between(x, neg_mult * x, pos_mult * x, facecolor='green', alpha=0.15,
                         zorder=3)
    elif area_parameter != 0:
        plt.plot(x, x - area_parameter, 'g:', lw=1.5, zorder=3)
        plt.plot(x, x + area_parameter, 'g:', lw=1.5, zorder=3)
        plt.fill_between(x, x - area_parameter, x + area_parameter, facecolor='green',
                         alpha=0.15,
                         zorder=3)
    #ax.set_xlim([0, maxval])
    #ax.set_ylim([0, maxval])

    # scatter
    ax.scatter(data_x, data_y, color="red", alpha=0.3, zorder=5)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, color='black', ls=':', lw=1, zorder=1)

    # ax = plt.gca()
    ax.set_xscale('log')
    ax.set_yscale('log')

    # setting ticks font properties
    # ax.set_xticklabels(ax.get_xticks(), self.f_props)
    # ax.set_yticklabels(ax.get_yticks(), self.f_props)

    # formatter
    strFormatter = plt.FormatStrFormatter('%d')
    logFormatter = plt.LogFormatterMathtext(base=10)
    ax.xaxis.set_major_formatter(strFormatter if not logscale else logFormatter)
    ax.yaxis.set_major_formatter(strFormatter if not logscale else logFormatter)

    # setting frame thickness
    # for i in six.itervalues(ax.spines):
    #     i.set_linewidth(1)

    # Show the plot
    plt.show()


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


def _scatter_reg_vs_tseitin_smooth(result_objs: List[_ResultObj], img_filepath):
    data_x = [r.sddnnf_nodecount for r in result_objs]
    data_x = np.array(data_x)
    xlabel = "number of nodes in sd-DNNF"
    data_y = [r.sddnnft_nodecount / r.sddnnf_nodecount * 100 for r in result_objs]
    data_y = np.array(data_y)
    ylabel = "nodes remaining in sd-DNNF+t (\%)"

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
    result_csv = "results/results_cnf_exp.csv"
    results = read_from_file(result_csv)
    results = _filter_duplicates(results)
    # _print_latex_table(results)
    _print_info(results)

    # comparison classic versus tseitin does not make sense to have regular
    # scatter because only the bottom triangle will be filled.
    print("reg vs tseitin")
    _scatter_reg_vs_tseitin(results, img_filepath="results/scatter_reg_vs_tseitin.pdf")
    # print("")
    # print("reg vs tseitin smooth")
    # _scatter_reg_vs_tseitin_smooth(results, img_filepath="results/scatter_reg_vs_tseitin_smooth.pdf")
    print("")
    print("prop vs tseitin")
    _scatter_prop_vs_tseitin(results, img_filepath="results/scatter_prop_vs_tseitin.pdf")

    # _scatterplot_pt(results)

