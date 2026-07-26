#!/usr/bin/env python3
"""CEGAR solver for Ramsey (3,t;n) instances.

Base CNF: triangle-freeness + optional degree bounds (exact encoder from
encode.py).  The independence constraint (no independent set of size t) is
NOT encoded upfront (C(n,t) clauses is far too many); instead we lazily add a
blocking clause "some pair inside S must be an edge" for each independent
t-set S found in a candidate model, until UNSAT or a genuine witness appears.

Soundness: every added clause is implied by the (3,t;n) property, and a model
is only reported SAT after an exhaustive independent-set check, so
  - "unsat" => no (3,t;n)-graph satisfies the seed clauses;
  - "sat"   => returned edge set is triangle-free with alpha < t
(both verified independently with verify_graph.check).
"""
import time
from itertools import combinations

from pysat.solvers import Cadical153

from encode import CNF, var_map, e, at_most_k, at_least_k


def _find_independent_t_set(n, t, adj):
    """Return one independent set of size t, or None.  Simple branch and
    bound on vertices in degree order; exact."""
    order = sorted(range(n), key=lambda v: sum(adj[v]))
    best = []

    def extend(cand, start):
        if len(cand) == t:
            return list(cand)
        # bound: remaining vertices
        if len(cand) + (len(order) - start) < t:
            return None
        for idx in range(start, len(order)):
            v = order[idx]
            if all(not adj[v][u] for u in cand):
                cand.append(v)
                r = extend(cand, idx + 1)
                if r:
                    return r
                cand.pop()
        return None

    return extend(best, 0)


def run(n, t, min_deg=None, max_deg=None, lex=False, seed_clauses=None,
        time_budget=None, dump_cnf=None, verbose=False):
    """Returns (result, edges, iterations, blocked_count) with result in
    {"sat","unsat","timeout"}."""
    vm, nv = var_map(n)
    cnf = CNF(nv)
    # triangle-freeness
    for i, j, k in combinations(range(n), 3):
        cnf.add([-e(vm, i, j), -e(vm, i, k), -e(vm, j, k)])
    # degree bounds
    for v in range(n):
        lits = [e(vm, v, u) for u in range(n) if u != v]
        if max_deg is not None:
            at_most_k(cnf, lits, max_deg)
        if min_deg is not None:
            at_least_k(cnf, lits, min_deg)
    if seed_clauses:
        for cl in seed_clauses:
            cnf.add(list(cl))

    if dump_cnf:
        with open(dump_cnf, "w") as f:
            f.write(f"p cnf {cnf.nv} {len(cnf.clauses)}\n")
            for cl in cnf.clauses:
                f.write(" ".join(map(str, cl)) + " 0\n")

    solver = Cadical153(bootstrap_with=cnf.clauses)
    t0 = time.time()
    iters = 0
    added = 0
    try:
        while True:
            if time_budget is not None and time.time() - t0 > time_budget:
                return "timeout", None, iters, added
            if not solver.solve():
                return "unsat", None, iters, added
            iters += 1
            model = set(l for l in solver.get_model() if l > 0)
            adj = [[False] * n for _ in range(n)]
            E = []
            for (i, j), var in vm.items():
                if var in model:
                    adj[i][j] = adj[j][i] = True
                    E.append((i, j))
            S = _find_independent_t_set(n, t, adj)
            if S is None:
                return "sat", E, iters, added
            solver.add_clause([e(vm, a, b) for a, b in combinations(S, 2)])
            added += 1
            if verbose and added % 100 == 0:
                print(f"  cegar: {added} blocked, {time.time()-t0:.0f}s",
                      flush=True)
    finally:
        solver.delete()
