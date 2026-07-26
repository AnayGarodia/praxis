#!/usr/bin/env python3
"""Emit DIMACS for SMS attack cases on (3,10,40).

case full : min-deg 4, max-deg 9 (implied bounds only; K3/I10 via SMS flags)
case d5   : additionally vertex 39 has degree exactly 5 with N(39)={34..38}
            independent, and global min-deg 5  (the 'minimum degree = 5' case;
            use SMS --initial-partition 34 5 1)
"""
import sys
from itertools import combinations
from encode import var_map, e, CNF, at_most_k, at_least_k

case = sys.argv[1]
out = open(sys.argv[2], "w")
n = 40
vm, nv = var_map(n)
cnf = CNF(nv)
mind = {"full": 4, "d5": 5}[case]
for v in range(n):
    lits = [e(vm, v, u) for u in range(n) if u != v]
    at_most_k(cnf, lits, 9)
    at_least_k(cnf, lits, mind)
if case == "d5":
    for u in range(39):
        lit = e(vm, u, 39)
        cnf.add([lit] if u >= 34 else [-lit])
    for a, b in combinations(range(34, 39), 2):
        cnf.add([-e(vm, a, b)])
out.write(f"p cnf {cnf.nv} {len(cnf.clauses)}\n")
for c in cnf.clauses:
    out.write(" ".join(map(str, c)) + " 0\n")
out.close()
