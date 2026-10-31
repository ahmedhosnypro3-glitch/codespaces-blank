#!/bin/bash
# Sweeper #41 loop: scan every 45-60s until the 2h budget ends.
NS=/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure
END=$(( $(date +%s) + 7200 ))
cd "$NS"
while [ "$(date +%s)" -lt "$END" ]; do
  python3 pool_run/sweeper41_scan.py
  sleep $((45 + RANDOM % 16))
done
echo "sweeper-41 budget ended $(date -u +%FT%TZ)" >> pool_run/sweeper41.log
wait
