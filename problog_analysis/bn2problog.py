#!/usr/bin/env python3
# encoding: utf-8
"""
bn2problog.py

Created by Wannes Meert on 06-03-2017.
Copyright (c) 2016 KU Leuven. All rights reserved.
"""
import itertools
import re
import sys
import os
import argparse
import logging
import abc
import time

from pyparsing import (
    Word,
    nums,
    ParseException,
    alphanums,
    OneOrMore,
    Or,
    Optional,
    dblQuotedString,
    Regex,
    Forward,
    ZeroOrMore,
    Suppress,
    removeQuotes,
    Group,
    ParserElement,
)

from problog_analysis.cpd import Variable, PGM, Factor

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

logger = logging.getLogger("be.kuleuven.cs.dtai.problog.bn2problog")


class HuginParser:

    re_comments = re.compile(r"""%.*?[\n\r]""")

    @staticmethod
    def rm_comments(string):
        return HuginParser.re_comments.sub("\n", string)

    def __init__(self, args):
        self.fn = args.input
        self.pgm = PGM()

        self.force_bool = False
        self.detect_bool = True
        self.drop_zero = False
        self.use_neglit = False

        if args.force_bool:
            self.force_bool = args.force_bool
        if args.nobooldetection:
            self.detect_bool = False
        if args.drop_zero:
            self.drop_zero = args.drop_zero
        if args.use_neglit:
            self.use_neglit = args.use_neglit

        self.domains = {}
        self.potentials = []

        S = Suppress

        p_optval = Or([dblQuotedString, S("(") + OneOrMore(Word(nums)) + S(")")])
        p_option = S(Group(Word(alphanums + "_") + S("=") + Group(p_optval) + S(";")))
        p_net = S(Word("net") + "{" + ZeroOrMore(p_option) + "}")
        p_var = Word(alphanums + "_")
        p_val = dblQuotedString.setParseAction(removeQuotes)
        p_states = Group(
            Word("states") + S("=") + S("(") + Group(OneOrMore(p_val)) + S(")") + S(";")
        )
        p_node = (
            S(Word("node"))
            + p_var
            + S("{")
            + Group(ZeroOrMore(Or([p_states, p_option])))
            + S("}")
        )
        p_par = Regex(r"\d+(\.\d*)?([eE][-+]?\d+)?")
        p_parlist = Forward()
        p_parlist << S("(") + Or([OneOrMore(p_par), OneOrMore(p_parlist)]) + S(")")
        p_data = S(Word("data")) + S("=") + Group(p_parlist) + S(";")
        p_potential = (
            S(Word("potential"))
            + S("(")
            + p_var
            + Group(Optional(S("|") + OneOrMore(p_var)))
            + S(")")
            + S("{")
            + p_data
            + S("}")
        )

        p_option.setParseAction(self.parse_option)
        p_node.setParseAction(self.parse_node)
        p_potential.setParseAction(self.parse_potential)

        self.parser = OneOrMore(Or([p_net, p_node, p_potential]))

    def parse_option(self, s, l, t):
        return None

    def parse_node(self, s, l, t):
        # print(t)
        rv = t[0]
        for key, val in t[1]:
            if key == "states":
                self.domains[rv] = val
                self.pgm.add_var(
                    Variable(
                        rv,
                        val,
                        detect_boolean=self.detect_bool,
                        force_boolean=self.force_bool,
                    )
                )

    def parse_potential(self, s, l, t):
        # print(t)
        rv = t[0]
        if rv not in self.domains:
            logger.error("Domain for {} not defined.".format(rv), halt=True)
            sys.exit(1)
        values = self.domains[rv]
        parents = t[1]
        parameters = t[2]
        if len(parents) == 0:
            table = list([float(p) for p in parameters])
            self.pgm.add_factor(Factor(self.pgm, rv, parents, table))
            return
        parent_domains = []
        for parent in parents:
            parent_domains.append(self.domains[parent])
        dom_size = len(values)
        table = {}
        idx = 0
        for val_assignment in itertools.product(*parent_domains):
            table[val_assignment] = [float(p) for p in parameters[idx : idx + dom_size]]
            idx += dom_size
        self.pgm.add_factor(Factor(self.pgm, rv, parents, table))

    def parse_string(self, text):
        text = HuginParser.rm_comments(text)
        result = None
        try:
            result = self.parser.parseString(text, parseAll=True)
        except ParseException as err:
            print(err)
        return result

    def parse(self):
        if self.fn is None:
            logger.warning("No filename given to parser")
            return None
        text = None
        logger.info("Start parsing ...")
        ts1 = time.clock()
        with open(self.fn, "r") as ifile:
            text = ifile.read()
        self.parse_string(text)
        ts2 = time.clock()
        logger.info("Parsing took {:.3f} sec".format(ts2 - ts1))
        return self.pgm

    @staticmethod
    def add_parser_arguments(parser):
        parser.add_argument(
            "--forcebool",
            dest="force_bool",
            action="store_true",
            help="Force binary nodes to be represented as Boolean predicates (0=f, 1=t)",
        )
        parser.add_argument(
            "--nobooldetection",
            action="store_true",
            help="Do not try to detect Boolean predicates (true/false, yes/no, ...)",
        )
        parser.add_argument(
            "--dropzero",
            dest="drop_zero",
            action="store_true",
            help="Drop zero probabilities (if possible)",
        )
        parser.add_argument(
            "--useneglit",
            dest="use_neglit",
            action="store_true",
            help="Use negative head literals",
        )
        parser.add_argument(
            "--allowdisjunct",
            action="store_true",
            help="Allow disjunctions in the body",
        )
        parser.add_argument(
            "--valueinatomname",
            action="store_false",
            help="Add value to atom name instead as a term (this removes invalid characters, "
                 "be careful that clean values do not overlap)",
        )
        parser.add_argument(
            "--adisfunction",
            action="store_true",
            help="Consider all ADs to represent functions of mutual exclusive conditions (like "
                 "in a Bayesian net)",
        )
        parser.add_argument("--compress", action="store_true", help="Compress tables")
        parser.add_argument(
            "--split", help="Comma-separated list of variable names to split on"
        )
        parser.add_argument(
            "--split-output",
            dest="splitoutput",
            action="store_true",
            help="Create one output file per connected network",
        )
        parser.add_argument("--output", "-o", help="Output file")
        parser.add_argument(
            "--output-format",
            default="problog",
            help="Output format ('problog', 'uai', 'hugin', 'xdsl', 'xmlbif')",
        )
        parser.add_argument("input", help="Input file")

    def run(self, args):
        pgm = self.parse()
        if args.compress:
            pgm = pgm.compress_tables(allow_disjunct=args.allowdisjunct)
        if pgm is None:
            logger.error("Could not build PGM structure")
            sys.exit(1)
        ofile = open(args.output, "w") if args.output else sys.stdout

        try:
            print(
                    pgm.to_problog(
                            drop_zero=self.drop_zero,
                            use_neglit=self.use_neglit,
                            value_as_term=args.valueinatomname,
                            ad_is_function=args.adisfunction,
                    ),
                    file=ofile,
            )
        finally:
            if args.output:
                ofile.close()


def main(argv=None):
    description = "Translate Bayesian net to ProbLog"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "--verbose", "-v", action="count", default=0, help="Verbose output"
    )
    parser.add_argument("--quiet", "-q", action="count", default=0, help="Quiet output")
    parser.add_argument(
        "--input-format", help="Input type ('hugin')"
    )
    HuginParser.add_parser_arguments(parser)
    args = parser.parse_args(argv)

    logger.setLevel(max(logging.INFO - 10 * (args.verbose - args.quiet), logging.DEBUG))
    logger.addHandler(logging.StreamHandler(sys.stdout))

    parser = HuginParser(args)
    parser.run(args)


def _parse_directory(dirpath):
    description = "Translate Bayesian net to ProbLog"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "--verbose", "-v", action="count", default=0, help="Verbose output"
    )
    parser.add_argument("--quiet", "-q", action="count", default=0, help="Quiet output")
    parser.add_argument(
        "--input-format", help="Input type ('hugin')"
    )
    HuginParser.add_parser_arguments(parser)
    args = parser.parse_args(None)
    logger.setLevel(max(logging.INFO - 10 * (args.verbose - args.quiet), logging.DEBUG))
    logger.addHandler(logging.StreamHandler(sys.stdout))

    for filename in os.listdir(dirpath):
        if filename.endswith('.net'):
            print(f"Parsing {filename}")
            args.input = os.path.join(dirpath, filename)
            args.output = os.path.join(dirpath, filename.replace('.net', '.pl'))
            parser = HuginParser(args)
            parser.run(args)


if __name__ == "__main__":
    sys.exit(main())
    # _parse_directory("../sources/bn_src/")
