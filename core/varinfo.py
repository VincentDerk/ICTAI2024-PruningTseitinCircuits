from typing import Optional, Set, Dict, Iterable


class VariableSetInfo:

    def __init__(self, node2dict: Optional[Dict] = None, tseitin_vars: Optional[Iterable] = None):
        self.node2dict = node2dict or dict()
        self.tseitin_vars = set(tseitin_vars) if tseitin_vars is not None else set()

    def __str__(self):
        return str(self.node2dict) + "\n" + str(self.tseitin_vars)
