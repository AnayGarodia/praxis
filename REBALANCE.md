# REBALANCE — shared priority queue over fixed ranges

Fixed index ranges produce order-of-magnitude load imbalance (confirmed by
solvers 5/8/12/15 and by the lead's own data). Switch to a claim-queue on
this git branch.

## Hardness data

`data/cube_times.txt`: one line per cube index, `<idx> <seconds|TIMEOUT>`,
from the lead's complete 15s-timeout sweep of all 1248 cubes. 361 solved
(these need NO further work — do not re-claim them); 887 TIMEOUT = the hard
core. Within the hard core, treat higher-index-density regions equally —
we have no finer ranking yet; L2 subcube counts observed 3.5k-518k.

## Claim protocol (git-based, no shared filesystem)

1. Pull this branch. Claims live in `claims/` as files named
   `claim_<idx>_<agent>.txt` (one cube per file, content = ISO timestamp).
2. To claim: pick the LOWEST unclaimed hard-core index (from hard_idx.txt,
   minus existing claims/ and results/), commit your claim file, push. On
   push conflict: pull --rebase; if your index got claimed by someone else,
   pick the next one. Claim at most 2 cubes at a time.
3. When a cube is refuted, commit `results/result_<idx>.txt`:
   `<idx> UNSAT <scheme> <total_seconds>` where scheme documents the split
   tree (e.g. `L1-timeout;cutoff160->8228sub;30s-timeouts:3;cutoff180->...`).
   Remove your claim file in the same commit.
4. Stale claims (>6h with no result) may be re-claimed by anyone; note the
   takeover in your claim file.
5. SAT rule unchanged: any solution line => STOP, verify with
   verify_graph.py, report to coordinator immediately.

## Cutoff guidance

- L1 cube -> subcubes: `--cube-line <idx> --simple-assignment-cutoff 160
  --prerun 5`. If subcube count would exceed ~120k (watch file growth), abort
  and use 135, then recurse two levels rather than one giant level.
- L2 subcubes: solve with `--cube-timeout 30`; recurse timeouts at cutoff
  190-200 with `--cube-line` into the L2 file.
- Never claim UNSAT from a truncated subcube file.

## Compute reality (lead's measurements)

L2 subcube batches run 1-3h per L1 cube on one core even when no L2 timeouts
occur; with ~50% L2 timeout stretches, per-cube cost is multi-hour to day.
887 hard cubes at these rates = CPU-weeks to CPU-months total. The earlier
12h figure was wrong — it extrapolated from the first 7 (easiest) hard cubes.
Plan accordingly: this rung completes only with sustained team throughput,
or with a smarter reformulation (see AUDIT.md on the proposed diam
constraint — rejected as unsound for now).
