#!/usr/bin/env python3
"""Neighborhood-gluing extender for the (3,10;40) min-degree ladder.

For a hypothetical (3,10;40)-graph G with a vertex v of degree d:
  H := G - N[v] is a (3,9; 39-d)-graph.
Conversely, G is determined by (H, cross edges between N(v) and V(H)):
vertices 0..38-d carry H, vertices 39-d..38 are N(v) (independent), vertex
39 is v (adjacent exactly to N(v)).  The free variables are the
(d x |V(H)|) cross edges.

Given a COMPLETE catalogue of (3,9;39-d)-graphs, refuting every gluing
refutes "some (3,10;40)-graph has a vertex of degree d" — one rung of the
ladder, by a route independent of the SMS cube pipeline (result quality is
then conditional only on the completeness of the input catalogue).

Usage:
  python3 glue.py <catalogue.g6> <d> [--range lo hi] [--time-budget s]
                  [--min-deg m] [-o results.txt]

Output: one line per catalogue index (1-based):
  <idx> UNSAT <iters> <blocked> <seconds>
  <idx> SAT <witness edge list>     <- STOP: decides the problem
  <idx> TIMEOUT <seconds>
Any SAT witness is re-verified with verify_graph.check before being
reported.
"""
import argparse
import sys
import time
from itertools import combinations

from g6 import load
from cegar import run
from encode import var_map, e
from verify_graph import check

def glue_one(HE, hn, d, min_deg, time_budget, N=40, T=10):
    """Try to extend the (3,T-1;hn)-graph H (edge list HE) by an independent
    d-set N(v) plus apex v of degree d.  hn + d + 1 must equal N."""
    assert hn + d + 1 == N
    vm, _ = var_map(N)
    Hset = set(HE)
    seed = []
    for a in range(hn):
        for b in range(a + 1, hn):
            lit = e(vm, a, b)
            seed.append([lit] if (a, b) in Hset else [-lit])
    # N(v) = {hn..hn+d-1} independent; v = 39 adjacent exactly to N(v)
    for a, b in combinations(range(hn, hn + d), 2):
        seed.append([-e(vm, a, b)])
    for u in range(N - 1):
        lit = e(vm, u, N - 1)
        seed.append([lit] if u >= hn else [-lit])
    # max degree T-1: N(u) is independent and alpha(G) <= T-1
    return run(N, T, min_deg=min_deg, max_deg=T - 1, lex=False,
               seed_clauses=seed, time_budget=time_budget)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("catalogue")
    ap.add_argument("d", type=int)
    ap.add_argument("--range", nargs=2, type=int, metavar=("LO", "HI"),
                    help="1-based inclusive catalogue index range")
    ap.add_argument("--time-budget", type=float, default=None)
    ap.add_argument("--min-deg", type=int, default=None,
                    help="already-proven min-degree rung (sound to assume "
                         "when attacking the next rung)")
    ap.add_argument("-o", "--out", default=None)
    ap.add_argument("--n", type=int, default=40)
    ap.add_argument("--t", type=int, default=10)
    args = ap.parse_args()
    N, T = args.n, args.t

    graphs = load(args.catalogue)
    lo, hi = (args.range if args.range else (1, len(graphs)))
    out = open(args.out, "w") if args.out else sys.stdout
    md = args.min_deg if args.min_deg is not None else args.d
    assert md <= args.d, "min-deg > d would contradict v's degree: vacuous"
    for idx in range(lo, hi + 1):
        hn, HE = graphs[idx - 1]
        t0 = time.time()
        res, E, iters, added = glue_one(HE, hn, args.d, md,
                                        args.time_budget, N=N, T=T)
        el = time.time() - t0
        if res == "sat":
            ok, msg = check(N, T, set(E))
            if not ok:
                print(f"{idx} INTERNAL-ERROR bogus witness: {msg}",
                      file=out, flush=True)
                sys.exit(2)
            print(f"{idx} SAT {sorted(E)}", file=out, flush=True)
            print("!!! SAT WITNESS — STOP AND REPORT !!!", file=sys.stderr)
            sys.exit(1)
        elif res == "unsat":
            print(f"{idx} UNSAT {iters} {added} {el:.1f}", file=out,
                  flush=True)
        else:
            print(f"{idx} TIMEOUT {el:.1f}", file=out, flush=True)
    if args.out:
        out.close()


if __name__ == "__main__":
    main()
