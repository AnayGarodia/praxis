# CLAIMS protocol — R(3,10) team, d=5 rung

1. Work ONLY the cube index range assigned to you by the coordinator.
   Indices are 1-based line numbers into the canonical cube file
   `data/d5cubes_deep.icnf` (sha256
   583c8c79a92b2fd5d7c3fd289b48cb79facded363ec06030a174ec930734b4c5).
   Verify the sha256 BEFORE starting; if it does not match, stop and report.

2. Record results in a file named `results_<lo>-<hi>.txt` (your assigned
   range), one line per cube index, in index order:

   ```
   <idx> UNSAT <seconds>
   <idx> TIMEOUT-SPLIT <n_subcubes> UNSAT <total_seconds>
   <idx> SAT <witness edge list>
   ```

   - `UNSAT`: smsg finished the cube with no solution line and no
     "Timeout reached" in the log.
   - `TIMEOUT-SPLIT ... UNSAT`: the cube timed out, you split it with
     `--cube-line <idx> --simple-assignment-cutoff 160 --prerun 5`, and ALL
     subcubes (count n_subcubes) returned UNSAT (recurse the same way for
     subcube timeouts; report the deepest scheme used in a trailing comment).
   - `SAT`: STOP EVERYTHING and report the witness immediately — it decides
     the whole problem (min degree 5 exists), and after independent
     verification would prove R(3,10) = 41.

3. Every cube in your range MUST have a line. No gaps. If you cannot finish a
   cube, write `<idx> OPEN` so the foreman can reassign it — never silently
   drop an index.

4. Keep raw smsg logs. The foreman may request them for audit. Solver-trust
   results become theorem-grade only after the coordinated DRAT replay, so
   logs are the interim evidence.

5. Solve command (after gunzip, from repo root; smsg build per BUILD.md):

   ```
   smsg --vertices 40 --initial-partition 34 5 1 \
     --dimacs cnf/sms40_d5.cnf \
     --forbidden-subgraph-file data/forb_k3.txt \
     --forbidden-induced-subgraph-file data/forb_i10.txt \
     --cube-file data/d5cubes_deep.icnf --cubes-range <lo> <hi> \
     --cube-timeout 15
   ```

   Then handle timeouts per (2). PITFALL: a few cubes explode when split
   (>500k subcubes / >1GB); cap generation (e.g. `| head -n 120000`) and if
   truncated, re-split with an intermediate cutoff (135) instead. Do not use a
   truncated subcube file for an UNSAT claim — truncation loses coverage.

6. Report `results_<lo>-<hi>.txt` back to the coordinator when your range is
   complete, plus interim copies every hour.
