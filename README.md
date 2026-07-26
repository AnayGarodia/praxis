# r310-team — coordinated attack on R(3,10) via the (3,10;40) SAT decision

Deciding whether a triangle-free graph on 40 vertices with independence
number <= 9 exists settles R(3,10) (known 40 <= R(3,10) <= 41).

Current campaign: the d=5 rung of the minimum-degree ladder — refute every
(3,10;40)-graph containing a vertex of degree 5. Split into 1248 SMS cubes.

Read in order:
1. `BUILD.md` — toolchain build (SMS commit-pinned + patch, kissat, drat-trim).
2. `STATUS.md` — cube ledger: what is already refuted, what remains.
3. `CLAIMS.md` — the work protocol; follow it exactly.

Key files:
- `cnf/sms40_d5.cnf` — base CNF (degree-5 case, see coordinator spec).
- `data/d5cubes_deep.icnf.gz` — THE canonical 1248-cube file (checksums in
  STATUS.md). Never regenerate.
- `data/hard_idx.txt` — the 887 hard cube indices; the rest are already done.
- `mk_case.py`, `encode.py` — exact encoders (Sinz counters, unit fixings).
- `verify_graph.py` — independent witness checker (use on any SAT claim).
- `hardworker.sh` — reference recursive split-and-solve worker.
- `sms_gmp_link.patch` — SMS build fix.

Banked so far (with certificates, held by lead agent): every (3,10;40)-graph
has min degree >= 5 (kissat + drat-trim verified; conditional only on GR2012
Theorem 3). All 1248 d=5 cubes swept at 15s timeout: zero SAT solutions.
