#!/usr/bin/env bash
# Certify-and-merge loop: scan every ~90s for 2h or until all 37 certified.
cd /home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure || exit 1
END=$(( $(date -u +%s) + 7200 ))
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) sweeper-cm2 loop start, budget until $(date -u -d @$END +%Y-%m-%dT%H:%M:%SZ)" >> pool_run/hygiene2.log
while [ "$(date -u +%s)" -lt "$END" ]; do
  out=$(python3 pool_run/sweeper_cm2_scan.py 2>&1)
  echo "$out" >> pool_run/hygiene2.log
  if echo "$out" | grep -q 'certified=37/37'; then
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) sweeper-cm2 loop: ALL 37 CERTIFIED, exiting" >> pool_run/hygiene2.log
    break
  fi
  sleep 90
done
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) sweeper-cm2 loop end" >> pool_run/hygiene2.log
