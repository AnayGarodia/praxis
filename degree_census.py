#!/usr/bin/env python3
"""Degree-census / structural-consequence calculator for (3,10;40)-graphs.

Converts a proven minimum-degree rung ("every (3,10;40)-graph has min degree
>= delta") into unconditional structural facts, using only:
  (F1) triangle-freeness: N(v) is independent, so deg(v) <= alpha(G) <= 9;
  (F2) for any vertex v of degree d, G - N[v] is a (3,9; 39-d)-graph
       (an independent 9-set there plus v would be a 10-set), hence
       39 - d <= 35, i.e. d >= 4  [R(3,9) = 36, GoRa2013];
  (F3) the edge identity e(G) = e(G - N[v]) + Z(v), where
       Z(v) = sum of deg(u) over u in N(v)  (N(v) is independent, so every
       edge incident to N(v) goes to v or to G - N[v], each counted once);
  (F4) the published exact values e(3,9,n) (GoRa2013, Table 4):
       these lower-bound e(G - N[v]).

All consequences are per-rung; the script prints the census for each rung
delta = 4..9 so the team can see what each new rung buys.

Label: the e(3,9,n) values and R(3,9)=36 are literature-trust (GoRa2013 =
Goedgebeur & Radziszowski, "New computational upper bounds for Ramsey
numbers R(3,K)", El. J. Comb. 20(3) 2013, arXiv:1210.5826).  Everything
else is elementary counting, re-derived here from scratch.
"""
import sys
from itertools import combinations

# e(3,9,n): minimum edges of a triangle-free graph on n vertices with
# independence <= 8.  n <= 26 from the cumulative small-case theorem;
# 27..35 computed by GoRa2013; n = 36 impossible (R(3,9) = 36).
E39 = {27: 61, 28: 68, 29: 77, 30: 86, 31: 95, 32: 104, 33: 118,
       34: 129, 35: 140}

N, ALPHA_MAX = 40, 9


def e39(n):
    if n > 35:
        raise ValueError(f"no (3,9;{n})-graph exists (R(3,9)=36)")
    if n in E39:
        return E39[n]
    raise KeyError(f"e(3,9,{n}) not tabulated here (only n>=27 needed)")


def edge_lower_bound(delta):
    """min over feasible min-degree values d >= delta of
    e(3,9,39-d) + d*d  (a vertex v of minimum degree d has
    Z(v) >= d * delta(G) = d*d and e(G-N[v]) >= e(3,9,39-d))."""
    per_d = {}
    for d in range(delta, ALPHA_MAX + 1):
        per_d[d] = e39(39 - d) + d * d
    return min(per_d.values()), per_d


def degree_census(delta, e_upper=180):
    """Enumerate all degree multisets (n_delta,...,n_9) consistent with:
    sum n_d = 40, and for the smallest degree d present, the edge bound
    e >= e(3,9,39-d) + d*d, and e = sum(d*n_d)/2 <= e_upper (default 180 =
    the 9-regular maximum, since deg <= 9)."""
    degs = list(range(delta, ALPHA_MAX + 1))
    feasible = []
    for counts in _compositions(N, len(degs)):
        s = sum(d * c for d, c in zip(degs, counts))
        if s % 2:
            continue
        edges = s // 2
        if edges > e_upper:
            continue
        dmin = next(d for d, c in zip(degs, counts) if c > 0)
        if edges < e39(39 - dmin) + dmin * dmin:
            continue
        feasible.append((dict((d, c) for d, c in zip(degs, counts) if c),
                         edges))
    return feasible


def _compositions(total, parts):
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in _compositions(total - first, parts - 1):
            yield (first,) + rest


def report(delta):
    lb, per_d = edge_lower_bound(delta)
    print(f"== Rung delta = {delta} (every (3,10;40)-graph has min degree "
          f">= {delta}) ==")
    print(f"  degree range: [{delta}, 9]  (upper: N(v) independent, "
          f"alpha <= 9)")
    for d in sorted(per_d):
        print(f"  if min degree = {d}: G-N[v] is a (3,9;{39-d})-graph, "
              f"e(G) >= e(3,9,{39-d}) + {d}^2 = {per_d[d]}")
    print(f"  ==> unconditional: e(3,10,40-graph) >= {lb}")
    census = degree_census(delta)
    edge_vals = sorted(set(e for _, e in census))
    print(f"  feasible degree multisets: {len(census)}; "
          f"edge counts {edge_vals[0]}..{edge_vals[-1]}")
    print()


if __name__ == "__main__":
    rungs = [int(a) for a in sys.argv[1:]] or [4, 5, 6, 7, 8, 9]
    for delta in rungs:
        report(delta)
