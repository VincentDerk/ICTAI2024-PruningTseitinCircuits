from typing import List
from raki_analysis.raki_report_script import read_from_file as raki_read_from_file
from problog_analysis.problog_report_script import read_from_file as problog_read_from_file
from cnf_analysis.cnf_exp_report_script import _filter_duplicates, read_from_file as cnf_read_from_file

import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.transforms as mtransforms
import numpy as np


def mscatter(x,y,ax=None, m=None, scale=0.75, **kw):
    """ source: https://github.com/matplotlib/matplotlib/issues/11155 """
    import matplotlib.markers as mmarkers
    if not ax: ax=plt.gca()
    sc = ax.scatter(x,y,**kw)
    if (m is not None) and (len(m)==len(x)):
        paths = []
        for marker in m:
            if isinstance(marker, mmarkers.MarkerStyle):
                marker_obj = marker
            else:
                marker_obj = mmarkers.MarkerStyle(marker)
                marker_obj = marker_obj
            path = marker_obj.get_path().transformed(
                        marker_obj.get_transform())
            scaled_path = mtransforms.Affine2D().scale(scale).transform_path(path)
            paths.append(scaled_path)
        sc.set_paths(paths)
    return sc


marker_map = {
    # marker, color, label, marker_size
    "/gnb/gnb_": ("^", "green", "gnb"),
    "/smokers/smokers_": ("x", "red", "smokers"),
    "/gh/gh_": (">", "blue", "gh"),
    "/lp2sat/smokers_": ("s", "yellow", "lp2sat/smokers"),
    "/lp2sat/tree_": ("^", "black", "lp2sat/tree"),
    "/tree/tree_": ("<", "orange", "tree"),
    "problog_src/powergrid-reliability": ("1", "purple", "reliability"),
    "MC2022_": ("2", "cyan", "MCC"),
    "MC2023_": ("2", "cyan", "MCC"),
}

default_marker = (".", "brown", "misc")

def _get_marker(instance_path):
    for key, value in marker_map.items():
        if key in instance_path:
            marker, color, label = value
            return marker
    # default
    return default_marker[0]


def _get_color(instance_path):
    for key, value in marker_map.items():
        if key in instance_path:
            marker, color, label = value
            return color
    # default
    return default_marker[1]


def _scatter_reg_vs_tseitin(result_objs, img_filepath):
    data_x = [r.ddnnf_nodecount for r in result_objs]
    data_x = np.array(data_x)
    xlabel = "number of nodes in d-DNNF"
    data_y = [r.ddnnft_nodecount / r.ddnnf_nodecount * 100 for r in result_objs]
    data_y = np.array(data_y)
    ylabel = "nodes remaining in d-DNNF+t (\%)"
    data_marker = [_get_marker(r.instance_name) for r in result_objs]
    data_color = [_get_color(r.instance_name) for r in result_objs]

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
    mscatter(data_x, data_y, ax=ax, m=data_marker, c=data_color, alpha=0.6, zorder=5)
    # ax.scatter(data_x, data_y, color="red", alpha=0.4, zorder=5, marker=".")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, color='black', ls=':', lw=1, zorder=1)
    ax.set_xscale('log')

    # formatter
    strFormatter = plt.FormatStrFormatter('%d')
    logFormatter = plt.LogFormatterMathtext(base=10)
    ax.xaxis.set_major_formatter(strFormatter if not logscale else logFormatter)

    # setting frame thickness
    for i in ax.spines.values():
        i.set_linewidth(1)

    # legend
    legend_handles = []
    for key, value in marker_map.items():
        marker, color, label = value
        legend_handles.append(mlines.Line2D([], [], color=color,
                                            linestyle='None', marker=marker, label=label))
    misc_marker, misc_color, misc_label = default_marker
    legend_handles.append(mlines.Line2D([], [], color=misc_color,
                                        linestyle="None", marker=misc_marker, label=misc_label))
    ax.legend(handles=legend_handles, ncol=3, loc='upper center', bbox_to_anchor=(0.4, -0.2))

    plt.savefig(img_filepath, bbox_inches='tight')
    # plt.show()


def _scatter_prop_vs_tseitin(result_objs, img_filepath):
    data_x = [r.ddnnfp_nodecount for r in result_objs]
    data_x = np.array(data_x)
    xlabel = "number of nodes in d-DNNF+p"
    data_y = [r.ddnnft_nodecount / r.ddnnfp_nodecount * 100 for r in result_objs]
    data_y = np.array(data_y)
    ylabel = "nodes remaining in d-DNNF+t (\%)"
    data_marker = [_get_marker(r.instance_name) for r in result_objs]
    data_color = [_get_color(r.instance_name) for r in result_objs]

    # results
    nb_improved = np.sum(data_y < 100)
    nb_same = np.sum(data_y == 100)
    nb_worse = np.sum(data_y > 100)
    avg_improvement = np.average(100 - data_y[data_y < 100])
    median_improvement = np.median(100 - data_y[data_y < 100])
    std_improvement = np.std(100 - data_y[data_y < 100])
    print(f"{len(data_y)} instances:")
    print(f"\tnb improved: {nb_improved};"
          f"\tremoved avg={avg_improvement:.3f}%"
          f"\tmedian={median_improvement:.3f}%"
          f"\tstd={std_improvement:.3f}%")
    print(f"\tnb same: {nb_same}")
    print(f"\tnb_worse: {nb_worse};")

    # plot
    logscale = True
    plt.style.use("../tex.mplstyle")
    fig, ax = plt.subplots()  # nrows=1, ncols=1, figsize=figsize)
    fig.set_figwidth(3.31)
    fig.set_figheight(3)

    # scatter
    mscatter(data_x, data_y, ax=ax, m=data_marker, c=data_color, alpha=0.6, zorder=5)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, color='black', ls=':', lw=1, zorder=1)
    ax.set_xscale('log')
    ax.set_ylim([0, 100])

    # formatter
    strFormatter = plt.FormatStrFormatter('%d')
    logFormatter = plt.LogFormatterMathtext(base=10)
    ax.xaxis.set_major_formatter(strFormatter if not logscale else logFormatter)

    # setting frame thickness
    for i in ax.spines.values():
        i.set_linewidth(1)

    # legend
    legend_handles = []
    for key, value in marker_map.items():
        marker, color, label = value
        legend_handles.append(mlines.Line2D([], [], color=color,
                                            linestyle='None', marker=marker, label=label))
    misc_marker, misc_color, misc_label = default_marker
    legend_handles.append(mlines.Line2D([], [], color=misc_color,
                                        linestyle="None", marker=misc_marker, label=misc_label))
    ax.legend(handles=legend_handles, ncol=3, loc='upper center', bbox_to_anchor=(0.4, -0.2))

    plt.savefig(img_filepath, bbox_inches='tight')
    # plt.show()


def _print_latex_table(result_objs, sort=True):
    if sort:
        result_objs.sort(key=lambda x: x.ddnnfp_nodecount / x.ddnnft_nodecount, reverse=True)
        # result_objs.sort(key=lambda x: x.ddnnf_nodecount, reverse=True)
    for result in result_objs:
        rel_compression = result.ddnnfp_nodecount / result.ddnnf_nodecount * 100
        rel_compression2 = result.ddnnft_nodecount / result.ddnnf_nodecount * 100
        tseitin_fraction = result.tseitin_var_count / result.var_count * 100
        name = result.instance_name
        new_name = name
        if "cnf/MC20" in name:
            mc_tag = "w" if "wmc" in name else ""
            is_public = "pu" if "public" in name else "pr"
            track_nr = 1 if "track1" in name else 2
            year = 23 if "mc2023" in name else 22
            digits = name[len(name)-7:-4]
            new_name = f"MCC{year}_{mc_tag}{is_public}{track_nr}_{digits}"
        elif "raki_aux_benchmarks/lp2sat/smokers" in name:
            new_name = name.replace(".lp", "").replace(".cnf", "").replace("../sources/raki_aux_benchmarks/", "").replace("_prob", "")
        elif "raki_aux_benchmarks/smokers/smokers" in name:
            new_name = name.replace(".lp", "").replace(".cnf", "").replace("../sources/raki_aux_benchmarks/", "").replace("_prob", "")
        elif "raki_aux_benchmarks/gh/gh" in name:
            new_name = name.replace("../sources/raki_aux_benchmarks/gh/", "").replace(".lp", "").replace(".cnf", "").replace("_prob", "")
        elif "raki_aux_benchmarks/gnb/gnb" in name:
            new_name = name.replace("../sources/raki_aux_benchmarks/gnb/", "").replace(".lp", "").replace(".cnf", "").replace("_prob", "")
        elif "raki_aux_benchmarks/tree/tree" in name:
            new_name = name.replace(".lp", "").replace(".cnf", "").replace("../sources/raki_aux_benchmarks/tree/", "")
        elif "raki_aux_benchmarks/lp2sat/tree" in name:
            new_name = name.replace(".lp", "").replace(".cnf", "").replace("../sources/raki_aux_benchmarks/", "")
        elif "powergrid" in name:
            new_name = (name.replace("../sources/problog_src/powergrid-reliability-latour2019/", "").
                        replace(".pl", "").replace("pgr-", "").replace("_gcc_",""))
        elif "problog_src" in name:
            new_name = name[len("../sources/problog_src/"):].replace("games/", "")

        msg = (f"{new_name} & {result.var_count} & {result.tseitin_var_count} ({tseitin_fraction:.0f}\%) & "
               f"{result.ddnnf_nodecount:,} & " +
               f"{result.ddnnfp_nodecount:,} ({rel_compression:.0f}\\%) & " +
               f"{result.ddnnft_nodecount:,} ({rel_compression2:.0f}\\%) \\\\")
        print(msg.replace(",", " ").replace("_", "\\_"))


def _print_info(result_objs):
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
    same_instances = [r.instance_name for r in result_objs if r.ddnnft_nodecount == r.ddnnfp_nodecount]
    print(f"Number of improvements: {num_improvements}/{nb_inst}")
    print(f"Number of same: {num_same}/{nb_inst}")
    print(f"Number of same of class gnb:{len(list(x for x in same_instances if '/gnb/gnb' in x))}")
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


if __name__ == "__main__":
    # results = cnf_read_from_file("../cnf_analysis/results/results_cnf_exp.csv")
    # results = _filter_duplicates(results)
    # results = raki_read_from_file("./results/results_raki_aux_benchmarks_exp.csv")
    # results.extend(problog_read_from_file("../problog_analysis/results/problog_exp.csv"))
    # _print_latex_table(results, sort=True)

    # read raki data
    result_csv = "./results/results_raki_aux_benchmarks_exp.csv"
    results = raki_read_from_file(result_csv)
    print(f"{len(results)} instances")
    print("instance".ljust(90) + "\t|ddnnf|\t|ddnnf+p| (remaining)\t|ddnn+t| (remaining)")
    for result in results:
        rel_compression = result.ddnnfp_nodecount / result.ddnnf_nodecount
        rel_compression2 = result.ddnnft_nodecount / result.ddnnf_nodecount
        msg = (f"{result.instance_name}".ljust(90) + f"\t{result.ddnnf_nodecount}\t" +
               f"\t{result.ddnnfp_nodecount}({rel_compression:.2f})" +
               f"\t{result.ddnnft_nodecount} ({rel_compression2:.2f})")
        print(msg)
    print("-- problog data --")
    # read problog data
    result_csv = "../problog_analysis/results/problog_exp.csv"
    results2 = problog_read_from_file(result_csv)
    print(f"{len(results2)} instances")
    print("instance".ljust(90) + "\t|ddnnf|\t|ddnnf+p| (remaining)\t|ddnn+t| (remaining)")
    for result in results2:
        rel_compression = result.ddnnfp_nodecount / result.ddnnf_nodecount
        rel_compression2 = result.ddnnft_nodecount / result.ddnnf_nodecount
        msg = (f"{result.instance_name}".ljust(90) + f"\t{result.ddnnf_nodecount}\t" +
               f"\t{result.ddnnfp_nodecount}({rel_compression:.2f})" +
               f"\t{result.ddnnft_nodecount} ({rel_compression2:.2f})")
        print(msg)
    # read nesy
    result_csv = "../nesy_analysis/results/countries_exp.csv"
    results3 = problog_read_from_file(result_csv)
    print(f"{len(results3)} instances")
    print("instance".ljust(90) + "\t|ddnnf|\t|ddnnf+p| (remaining)\t|ddnn+t| (remaining)")
    for result in results3:
        rel_compression = result.ddnnfp_nodecount / result.ddnnf_nodecount
        rel_compression2 = result.ddnnft_nodecount / result.ddnnf_nodecount
        msg = (f"{result.instance_name}".ljust(90) + f"\t{result.ddnnf_nodecount}\t" +
               f"\t{result.ddnnfp_nodecount}({rel_compression:.2f})" +
               f"\t{result.ddnnft_nodecount} ({rel_compression2:.2f})")
        print(msg)
    # read CNFs
    result_csv = "../cnf_analysis/results/results_cnf_exp.csv"
    results4 = cnf_read_from_file(result_csv)
    results4 = _filter_duplicates(results4)
    print(f"{len(results4)} instances")
    print("instance".ljust(90) + "\t|ddnnf|\t|ddnnf+p| (remaining)\t|ddnn+t| (remaining)")
    for result in results4:
        rel_compression = result.ddnnfp_nodecount / result.ddnnf_nodecount
        rel_compression2 = result.ddnnft_nodecount / result.ddnnf_nodecount
        msg = (f"{result.instance_name}".ljust(90) + f"\t{result.ddnnf_nodecount}\t" +
               f"\t{result.ddnnfp_nodecount}({rel_compression:.2f})" +
               f"\t{result.ddnnft_nodecount} ({rel_compression2:.2f})")
        print(msg)
    print("----------------\n\n")
    results.extend(results2)
    results.extend(results3)
    results.extend(results4)
    _print_info(results)
    print("----------------")
    print("reg vs tseitin")
    _scatter_reg_vs_tseitin(results, "./results/global_reg_vs_tseitin.pdf")
    print("")
    print("prop vs tseitin")
    _scatter_prop_vs_tseitin(results, "./results/global_prop_vs_tseitin.pdf")
