#!/bin/bash
# Usage: enum34_worker.sh <worker_id> <num_workers> <cube_file> <outdir>
# Solves the (3,9;34) enumeration cube <idx> for every idx = worker_id mod
# num_workers (1-based line numbers), with --all-graphs, no timeout.
# Solutions stream into <outdir>/sol_<idx>.out; "DONE idx" markers into
# <outdir>/done_<idx> for the ledger.
set -u
W=$1; NW=$2; CF=$3; OD=$4
mkdir -p "$OD"
S="$HOME/.local/bin/smsg --vertices 34 --all-graphs --dimacs /tmp/t34.cnf \
   --forbidden-subgraph-file data/forb_k3.txt \
   --forbidden-induced-subgraph-file data/forb_i9.txt"
NC=$(wc -l < "$CF")
for ((idx=1; idx<=NC; idx++)); do
  if [ $(( (idx - 1) % NW )) -eq "$W" ] && [ ! -s "$OD/done_$idx" ]; then
    $S --cube-file "$CF" --cube-line "$idx" > "$OD/sol_$idx.out" 2>&1
    rc=$?
    if [ $rc -eq 0 ] || grep -q "Number of graphs" "$OD/sol_$idx.out"; then
      echo "$rc" > "$OD/done_$idx"
    fi
  fi
done
