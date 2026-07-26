#!/bin/bash
# Usage: hardworker.sh <worker_id> <num_workers>
# Processes hard cube indices (data/hard_idx.txt) round-robin.
# For each: split into subcubes at cutoff 200, then solve all subcubes
# with 30s timeout. Subcube-timeouts recorded for level 3.
cd ~/ramsey
W=$1; NW=$2
S="$HOME/.local/bin/smsg --vertices 40 --initial-partition 34 5 1 --dimacs cnf/sms40_d5.cnf --forbidden-subgraph-file data/forb_k3.txt --forbidden-induced-subgraph-file data/forb_i10.txt"
mkdir -p work
i=0
while read idx; do
  if [ $((i % NW)) -eq $W ]; then
    sub=work/sub$idx.icnf
    log=work/solve$idx.log
    if [ ! -s work/done$idx ]; then
      $S --cube-file data/d5cubes_deep.icnf --cube-line $idx \
         --simple-assignment-cutoff 160 --prerun 5 2>/dev/null \
         | grep "^a " | head -n 120000 > $sub
      nc=$(wc -l < $sub)
      echo "$(date +%T) idx=$idx subcubes=$nc" >> logs/hardw$W.log
      if [ $nc -ge 120000 ]; then
        # generation was truncated: unsound to rely on; flag for manual deep handling
        echo "TRUNCATED idx=$idx" >> logs/hardw$W.log
        echo "truncated" > work/done$idx
        rm -f $sub
        i=$((i+1)); continue
      fi
      $S --cube-file $sub --cubes-range 1 $nc --cube-timeout 30 > $log 2>&1
      to=$(grep -c "Timeout reached" $log)
      sols=$(grep -c '^\[' $log)
      echo "$(date +%T) idx=$idx done timeouts=$to sols=$sols" >> logs/hardw$W.log
      if [ "$sols" != "0" ]; then echo "SAT-FOUND idx=$idx" >> logs/hardw$W.log; fi
      echo "to=$to sols=$sols" > work/done$idx
      if [ "$to" = "0" ]; then rm -f $log $sub; fi
    fi
  fi
  i=$((i+1))
done < data/hard_idx.txt
echo "WORKER $W COMPLETE" >> logs/hardw$W.log
