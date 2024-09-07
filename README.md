# ICTAI2024 - Pruning Boolean d-DNNF Circuits Through Tseitin-Awareness

This repository contains the code and data instances of the paper published at the ICTAI 2024 conference, "Pruning Boolean d-DNNF Circuits Through Tseitin-Awareness" by Vincent Derkinderen.

The idea is quite simple: if the unweighted model count of a node in the d-DNNF is equivalent to `2**|Y|`, with `|Y|` the number of non-Tseitin variables in the node's scope, then the node is marked as Tseitin artifact and can be removed.


## Noisy-OR

Run `noisy_or_exp_script.py` in the `problog_analysis` folder to execute the noisy-or experiment. The results are stored in `results/noisy_or.csv`. The script `noisy_or_exp_report_script.py` converts those results into the plot (`results/noisy_or.pdf`) used in the paper.

## Bayesian networks

Run `bn_no_tseitin_exp_script.py` in the `problog_analysis` folder to execute the Bayesian network experiment. The results are stored in `results/bn_no_tseitin_exp.csv`. The script `bn_no_tseitin_report_script.py` converts those results into the plot (`results/bn_no_tseitin_exp.pdf`) used in the extended version of the paper.

## NeSy/Countries

Run `countries_exp.py` in the `nesy_analysis` folder to execute the Countries knowledge graph experiment. The results are stored in `results/countries_exp.csv`. The script `countries_report.py` reads those results and generates a table.

## MCC

The `filter_cnfs_script.py` script in the `cnf_analysis` folder filters paths of relevant CNF files, stored in `results/tseitin-var-counts-mcc-filtered.csv`. The `cnf_exp_script.py` script runs the filtered MCC dataset, storing results in `results/results_cnf_exp.csv`. The `cnf_exp_report_script.py` script then reports on the results, creating `results/scatter_reg_vs_tseitin.pdf` and `results/scatter_prop_vs_tseitin.pdf`.

## CNFT

Run `problog_exp_script.py` in the `problog_analysis` folder to execute part of the CNFT experiment. The results are stored in `results/problog_exp.csv`.
Run `raki_exp_script.py` in the `raki_analysis` folder to execute part of the CNFT experiment. The results are stored in `results/results_cnf_exp.csv`, which you can rename to `results_raki_aux_benchmarks_exp.csv`.
The `global_report_script.py` script then prints information and a table for the CNFT and MCC dataset. The `combined_report_script.py` creates the CNFT scatter plots used in the paper.
