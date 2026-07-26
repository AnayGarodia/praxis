#!/usr/bin/env python3
"""Degree-delta vertex extension attack on (3,10,40).

If G is a (3,10,40)-graph (triangle-free, alpha<=9) with a vertex v of degree
d, then G - N[v] is a triangle-free graph on 39-d vertices with alpha<=8,
i.e. a (3,9,39-d)-graph.  For d=4 that graph has 35 vertices and the unique
(3,9,35)-graph is known (McKay's r39_35.g6; enumeration completeness is
literature-trust). So the d=4 case reduces to: fix H on vertices 0..34,
neighbors N={35,36,37,38} (independent), v=39 adjacent to exactly N.
Free variables: cross edges N x V(H). Solve with CEGAR on alpha<=9.

UNSAT => every (3,10,40)-graph has min degree >= 5 (conditional on
completeness of the (3,9,35) enumeration).
"""
import sys
from itertools import combinations
from g6 import load
from cegar import run
from encode import var_map, e


def main(time_budget=None):
    n, t = 40, 10
    graphs = load("data/r39_35.g6")
    assert len(graphs) == 1
    hn, HE = graphs[0]
    assert hn == 35
    vm, _ = var_map(n)
    Hset = set(HE)
    seed = []
    # fix H on 0..34
    for a in range(35):
        for b in range(a + 1, 35):
            lit = e(vm, a, b)
            seed.append([lit] if (a, b) in Hset else [-lit])
    # v=39 adjacent exactly to 35..38
    for u in range(39):
        lit = e(vm, u, 39)
        seed.append([lit] if u >= 35 else [-lit])
    # N independent
    for a, b in combinations(range(35, 39), 2):
        seed.append([-e(vm, a, b)])
    res, E, it, added = run(n, t, min_deg=4, max_deg=9, lex=False,
                            seed_clauses=seed, time_budget=time_budget,
                            dump_cnf="cnf/extend40_d4.cnf")
    print("RESULT:", res, "iters", it, "blocked", added, flush=True)
    if res == "sat":
        print("EDGES", E)


if __name__ == "__main__":
    tb = float(sys.argv[1]) if len(sys.argv) > 1 else None
    main(tb)
