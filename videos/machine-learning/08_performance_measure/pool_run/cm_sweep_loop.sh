#!/bin/bash
# Certify-and-merge sweeper loop for 08_performance_measure — one scan every ~90s.
# Stops when all 37 slides are certified in final_deck_ledger.json or after ~2h.
cd "$(dirname "$0")/.." || exit 1
START=$(date +%s)
while true; do
  python3 pool_run/cm_sweep_scan.py >> pool_run/cm_sweep_loop.out 2>&1
  rc=$?
  now=$(date +%s)
  if [ "$rc" -eq 0 ]; then
    echo "$(date -u +%FT%TZ) all 37 certified, loop exiting" >> pool_run/hygiene2.log
    break
  fi
  if [ $((now - START)) -ge 7200 ]; then
    echo "$(date -u +%FT%TZ) 2h budget reached, loop exiting" >> pool_run/hygiene2.log
    break
  fi
  sleep 90
done
