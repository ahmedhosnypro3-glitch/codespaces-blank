#!/bin/bash
# Certify-and-merge sweep loop: one pass every ~90s until 2h budget ends
# or all 37 slides certified. All writes inside this namespace.
cd /home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure
DEADLINE=$(( $(date -u +%s) + 7200 ))
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) hygiene2 cert-sweep loop start, deadline $(date -u -d @$DEADLINE +%Y-%m-%dT%H:%M:%SZ)" >> pool_run/hygiene2.log
while true; do
  python3 pool_run/hygiene2_cert_sweep.py
  rc=$?
  now=$(date -u +%s)
  if [ $rc -eq 0 ]; then
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) all 37 slides certified; loop exit" >> pool_run/hygiene2.log
    break
  fi
  if [ $now -ge $DEADLINE ]; then
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) 2h budget exhausted; loop exit" >> pool_run/hygiene2.log
    break
  fi
  sleep 90
done
