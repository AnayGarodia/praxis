#!/usr/bin/env python3
"""Tools for building and validating the (3,9;34) catalogue from smsg output.

Subcommands:
  collect <smsg.out> <n> [-t 9] -o out.g6
      Parse smsg solution lines "[(0,9),(0,10),...]" into graph6, after
      re-verifying each graph independently (triangle-free, alpha <= 8).
      Dedupe up to isomorphism via nauty's shortg.
  census <file.g6>
      Print edge-count census (for comparison against GoRa2013 Table 14).
  deletions <r39_35.g6> <catalogue.g6>
      Check every one-vertex-deleted subgraph of the unique (3,9;35)-graph
      appears in the catalogue (a necessary completeness condition).
"""
import ast
import shutil
import subprocess
import sys
import tempfile

from g6 import load
from verify_graph import check


def edges_to_g6(n, E):
    Eset = set((min(a, b), max(a, b)) for a, b in E)
    bits = []
    for j in range(1, n):
        for i in range(j):
            bits.append(1 if (i, j) in Eset else 0)
    while len(bits) % 6:
        bits.append(0)
    chars = []
    assert n < 63
    chars.append(chr(n + 63))
    for k in range(0, len(bits), 6):
        x = 0
        for b in bits[k:k + 6]:
            x = (x << 1) | b
        chars.append(chr(x + 63))
    return "".join(chars)


def _tool(name):
    return name if shutil.which(name) else "nauty-" + name


def shortg(g6_lines):
    """Canonical dedupe via nauty shortg; returns sorted unique canonical
    forms."""
    with tempfile.NamedTemporaryFile("w", suffix=".g6", delete=False) as f:
        f.write("\n".join(g6_lines) + "\n")
        path = f.name
    out = subprocess.run([_tool("shortg"), "-q", path, path + ".can"],
                         check=True)
    del out
    with open(path + ".can") as f:
        return [l.strip() for l in f if l.strip()]


def labelg_one(line):
    p = subprocess.run([_tool("labelg"), "-q"], input=line + "\n",
                       capture_output=True, text=True, check=True)
    return p.stdout.strip()


def cmd_collect(argv):
    src, n = argv[0], int(argv[1])
    t = int(argv[argv.index("-t") + 1]) if "-t" in argv else 9
    out = argv[argv.index("-o") + 1]
    g6s = []
    bad = 0
    for line in open(src):
        line = line.strip()
        if not line.startswith("[("):
            continue
        E = ast.literal_eval(line)
        ok, msg = check(n, t, set(E))
        if not ok:
            print(f"REJECT (verify failed): {msg}", file=sys.stderr)
            bad += 1
            continue
        g6s.append(edges_to_g6(n, E))
    uniq = shortg(g6s) if g6s else []
    with open(out, "w") as f:
        f.write("\n".join(uniq) + ("\n" if uniq else ""))
    print(f"parsed {len(g6s)} verified solutions ({bad} rejected), "
          f"{len(uniq)} non-isomorphic -> {out}")


def cmd_census(argv):
    graphs = load(argv[0])
    from collections import Counter
    c = Counter(len(E) for _, E in graphs)
    for e in sorted(c):
        print(f"e={e}: {c[e]}")
    print(f"total: {len(graphs)}")


def cmd_deletions(argv):
    big_path, cat_path = argv[0], argv[1]
    (bn, BE), = load(big_path)
    cat = set(labelg_one(l.strip()) for l in open(cat_path) if l.strip())
    missing = 0
    seen = set()
    for v in range(bn):
        keep = [u for u in range(bn) if u != v]
        remap = {u: i for i, u in enumerate(keep)}
        E = [(remap[a], remap[b]) for a, b in BE if a != v and b != v]
        ok, msg = check(bn - 1, 9, set(E))
        assert ok, msg
        can = labelg_one(edges_to_g6(bn - 1, E))
        seen.add(can)
        if can not in cat:
            missing += 1
            print(f"MISSING: deletion of vertex {v}")
    print(f"{bn} deletions, {len(seen)} distinct, missing from "
          f"catalogue: {missing}")


if __name__ == "__main__":
    cmd = sys.argv[1]
    {"collect": cmd_collect, "census": cmd_census,
     "deletions": cmd_deletions}[cmd](sys.argv[2:])
