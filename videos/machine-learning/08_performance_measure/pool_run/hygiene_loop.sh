#!/bin/bash
# Ledger/hygiene loop for 08_performance_measure — one cross-check cycle every 90s.
# Append-only: never deletes or rewrites banked rows; only appends to hygiene.log.
cd "$(dirname "$0")/.." || exit 1
while true; do
  ts=$(date -u +%FT%TZ)
  line=$(python3 pool_run/hygiene_scan.py 2>&1)
  printf '%s %s\n' "$ts" "$line" >> pool_run/hygiene.log
  sleep 90
done
