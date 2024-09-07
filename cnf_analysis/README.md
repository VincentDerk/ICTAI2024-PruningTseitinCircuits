The `cnf2tseitin_script.py` file analyses the CNF instances in `./cnf/` and extracts potential tseitin variables.
The analysis results are stored in `tseitin-var-counts-mcc.csv`.
We assume that a tseitin procedure introduces many tseitin variables.
Therefore, we filter out instances with few potential tseitin variables.
The remaining instances are stored in `tseitin-var-counts-mcc-filtered.csv`.

