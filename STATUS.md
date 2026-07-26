# STATUS — d=5 rung of (3,10;40), cube ledger

Canonical cube file: `data/d5cubes_deep.icnf.gz` (gunzip first).
Uncompressed sha256:
`583c8c79a92b2fd5d7c3fd289b48cb79facded363ec06030a174ec930734b4c5`
1248 cubes, 1-indexed by line number. Do NOT regenerate cubes — generation is
not bit-reproducible; always use this file.

## Ledger (as of 2026-07-26 ~03:30 UTC)

- EASY SET (refuted, UNSAT in <= 15s each, 0 solutions): every index in
  1..1248 that is NOT listed in `data/hard_idx.txt` — 361 cubes. Refuted by
  the lead agent's 15s-timeout sweep.
- HARD CORE: the 887 indices in `data/hard_idx.txt`
  (sha256 `c40b40873ffb8de1755f50faebca38e6913c2f59cb6897352f4bd3c2c20c73fe`).
- Hard-core indices already fully refuted by the lead agent's recursive
  pipeline: see `data/hard_done_idx.txt` (currently 11:
  1 2 3 6 7 12 14 15 60 61 62). Treat these as done but re-doing them is
  harmless (UNSAT is idempotent).
- SAT solutions found so far anywhere: NONE.

## Authoritative assignment (2026-07-26)

- Lead agent: hard-core indices in 1..301 (1-based into the canonical cube
  file) plus the ongoing global hard-core recursion already started.
- Indices 302-312: SOLVER 4 (lead cedes the overlap; do not double-assign).
- All other ranges: per coordinator's assignment sheet; the claim-queue in
  REBALANCE.md supersedes fixed ranges once adopted.

## What a completed run yields

If every one of the 1248 cubes is UNSAT: **every (3,10;40)-graph has minimum
degree >= 6** (the deg-5 case with vertex 39 as the deg-5 vertex is WLOG by
vertex relabeling; its neighborhood independence is WLOG by triangle-freeness).
Label: computer-assisted, solver-trust (SMS minimality propagator + Glasgow;
no DRAT). A DRAT-certified replay is a separate follow-up task owned by the
lead agent.

Already banked previously: minimum degree >= 5 for every (3,10;40)-graph
(kissat + drat-trim verified), conditional only on GR2012 Theorem 3
(uniqueness of the (3,9;35)-graph).
