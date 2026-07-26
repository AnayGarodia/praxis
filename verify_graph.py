#!/usr/bin/env python3
"""Independent checker: given n, t and an edge set (or a DIMACS model),
verify triangle-freeness and independence number < t by brute force.
Completely independent of encode.py logic (recomputes from scratch)."""
import sys
from itertools import combinations


def var_of(n, i, j):
    # must match encoder's dense order: (0,1),(0,2),...,(0,n-1),(1,2),...
    c = 0
    for a in range(n):
        for b in range(a + 1, n):
            c += 1
            if (a, b) == (i, j):
                return c
    raise ValueError


def edges_from_model(n, model_lits):
    pos = set(l for l in model_lits if l > 0)
    E = set()
    c = 0
    for a in range(n):
        for b in range(a + 1, n):
            c += 1
            if c in pos:
                E.add((a, b))
    return E


def check(n, t, E):
    adj = [[False] * n for _ in range(n)]
    for a, b in E:
        adj[a][b] = adj[b][a] = True
    for i, j, k in combinations(range(n), 3):
        if adj[i][j] and adj[i][k] and adj[j][k]:
            return False, f"triangle {i},{j},{k}"
    for S in combinations(range(n), t):
        if all(not adj[a][b] for a, b in combinations(S, 2)):
            return False, f"independent set {S}"
    return True, "OK: triangle-free and alpha <= %d" % (t - 1)


if __name__ == "__main__":
    n, t = int(sys.argv[1]), int(sys.argv[2])
    lits = []
    for line in open(sys.argv[3]):
        if line.startswith("v"):
            lits += [int(x) for x in line.split()[1:] if x != "0"]
    E = edges_from_model(n, lits)
    ok, msg = check(n, t, E)
    print(msg, f"({len(E)} edges)")
    sys.exit(0 if ok else 1)
