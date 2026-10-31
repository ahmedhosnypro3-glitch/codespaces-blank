#!/bin/bash
# Certify-and-merge sweep loop for 08_performance_measure — one scan every ~90s
# for a 2h budget. All output (scan summaries + merge lines, UTC-timestamped) is
# appended by the python script itself to pool_run/hygiene2.log.
cd "$(dirname "$0")/.." || exit 1
DEADLINE=$(( $(date -u +%s) + 7200 ))
while [ "$(date -u +%s)" -lt "$DEADLINE" ]; do
  python3 pool_run/sweeper_dualpass_merge.py 2>>pool_run/hygiene2_sweeper.err
  # keep ~90s between scan starts
  now=$(date -u +%s)
  if [ "$now" -lt "$DEADLINE" ]; then
    sleep 90
  fi
done
echo "$(date -u +%FT%TZ) dualpass sweep loop ended (2h budget reached)" >> pool_run/hygiene2.log
