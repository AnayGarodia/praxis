#!/usr/bin/env python3
"""Exact CNF encoder for Ramsey (3,t;n) arrow decision.

Variables: e(i,j) for 0<=i<j<n.
Clauses:
  - triangle-free: for each i<j<k: (-e_ij v -e_ik v -e_jk)
  - independence < t: for each t-subset S: OR of e over pairs in S
Optional: per-vertex degree bounds (Sinz sequential counters, standard+sound),
fixing vertex 0's neighborhood (sound modulo vertex permutation symmetry).
"""
import sys
from itertools import combinations


def var_map(n):
    vm = {}
    c = 0
    for i in range(n):
        for j in range(i + 1, n):
            c += 1
            vm[(i, j)] = c
    return vm, c


def e(vm, i, j):
    return vm[(i, j)] if i < j else vm[(j, i)]


class CNF:
    def __init__(self, nv):
        self.nv = nv
        self.clauses = []

    def new_var(self):
        self.nv += 1
        return self.nv

    def add(self, cl):
        self.clauses.append(cl)


def at_most_k(cnf, lits, k):
    """Sinz 2005 sequential at-most-k. Sound and standard."""
    n = len(lits)
    if k >= n:
        return
    if k == 0:
        for l in lits:
            cnf.add([-l])
        return
    s = [[cnf.new_var() for _ in range(k)] for _ in range(n)]
    cnf.add([-lits[0], s[0][0]])
    for j in range(1, k):
        cnf.add([-s[0][j]])
    for i in range(1, n):
        cnf.add([-lits[i], s[i][0]])
        cnf.add([-s[i - 1][0], s[i][0]])
        for j in range(1, k):
            cnf.add([-lits[i], -s[i - 1][j - 1], s[i][j]])
            cnf.add([-s[i - 1][j], s[i][j]])
        cnf.add([-lits[i], -s[i - 1][k - 1]])


def at_least_k(cnf, lits, k):
    at_most_k(cnf, [-l for l in lits], len(lits) - k)


def lex_adjacent(cnf, vm, n):
    """Partial lex-leader: for each i, row_i >=lex row_{i+1} on columns
    excluding {i,i+1}. Sound: every graph has an isomorphic copy whose
    adjacency matrix is the lex-leader under vertex permutations, and the
    lex-leader satisfies these constraints for adjacent transpositions."""
    for i in range(n - 1):
        j = i + 1
        cols = [c for c in range(n) if c != i and c != j]
        # row_i >= lex row_j : a_k = e(i,c_k), b_k = e(j,c_k)
        # eq_k: prefix equal up to k
        prev_eq = None
        for k, c in enumerate(cols):
            a, b = e(vm, i, c), e(vm, j, c)
            if prev_eq is None:
                # not (a<b) at first position: b -> a
                cnf.add([a, -b])
            else:
                cnf.add([-prev_eq, a, -b])
            if k == len(cols) - 1:
                break
            eq = cnf.new_var()
            # eq <-> (prev_eq &) a==b   (only -> direction needed for soundness
            # of "if all previous equal then a>=b", but define both for safety)
            if prev_eq is None:
                cnf.add([-eq, a, -b])
                cnf.add([-eq, -a, b])
                cnf.add([eq, a, b])
                cnf.add([eq, -a, -b])
            else:
                cnf.add([-eq, prev_eq])
                cnf.add([-eq, a, -b])
                cnf.add([-eq, -a, b])
                cnf.add([eq, -prev_eq, a, b])
                cnf.add([eq, -prev_eq, -a, -b])
            prev_eq = eq


def encode(n, t, out, min_deg=None, max_deg=None, fix_deg0=None, lex=False,
           no_indep=False):
    vm, nv = var_map(n)
    cnf = CNF(nv)
    for i, j, k in combinations(range(n), 3):
        cnf.add([-e(vm, i, j), -e(vm, i, k), -e(vm, j, k)])
    if not no_indep:
        for S in combinations(range(n), t):
            cnf.add([e(vm, a, b) for a, b in combinations(S, 2)])
    if max_deg is not None or min_deg is not None:
        for v in range(n):
            lits = [e(vm, v, u) for u in range(n) if u != v]
            if max_deg is not None:
                at_most_k(cnf, lits, max_deg)
            if min_deg is not None:
                at_least_k(cnf, lits, min_deg)
    if fix_deg0 is not None:
        for u in range(1, n):
            cnf.add([e(vm, 0, u)] if u <= fix_deg0 else [-e(vm, 0, u)])
    if lex:
        lex_adjacent(cnf, vm, n)
    out.write(f"p cnf {cnf.nv} {len(cnf.clauses)}\n")
    w = out.write
    for c in cnf.clauses:
        w(" ".join(map(str, c)) + " 0\n")


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("n", type=int)
    ap.add_argument("t", type=int)
    ap.add_argument("--min-deg", type=int)
    ap.add_argument("--max-deg", type=int)
    ap.add_argument("--fix-deg0", type=int, help="vertex0 adjacent exactly to 1..d")
    ap.add_argument("--lex", action="store_true")
    ap.add_argument("--no-indep", action="store_true")
    ap.add_argument("-o", "--out", default="-")
    a = ap.parse_args()
    out = sys.stdout if a.out == "-" else open(a.out, "w")
    encode(a.n, a.t, out, a.min_deg, a.max_deg, a.fix_deg0, a.lex, a.no_indep)
    if out is not sys.stdout:
        out.close()
