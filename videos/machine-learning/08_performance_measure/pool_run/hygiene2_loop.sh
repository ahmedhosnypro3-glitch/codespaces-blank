#!/bin/bash
# Deeper ledger/hygiene loop for 08_performance_measure — one cross-check cycle every 120s.
# Appends exactly one timestamped line per cycle to pool_run/hygiene2.log
#   date -u +%FT%TZ certified=N/37 consistent=T/F fixes=K
# Scan diagnostics go to pool_run/hygiene2_detail.log. Append-only: never deletes
# or rewrites banked rows. Distinct from hygiene_loop.sh (90s lane) — do not run both scans twice.
cd "$(dirname "$0")/.." || exit 1
while true; do
  ts=$(date -u +%FT%TZ)
  line=$(python3 pool_run/hygiene2_scan.py 2>>pool_run/hygiene2_detail.log)
  printf '%s %s\n' "$ts" "$line" >> pool_run/hygiene2.log
  sleep 120
done
