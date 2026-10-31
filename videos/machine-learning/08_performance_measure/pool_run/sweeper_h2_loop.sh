#!/bin/bash
# Certify-and-merge sweep loop: one scan pass every ~90s, up to 2h budget,
# until all 37 slides are certified in final_deck_ledger.json.
cd /home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure || exit 1
START=$(date -u +%s)
BUDGET=7200
while true; do
  python3 pool_run/sweeper_h2.py
  NOW=$(date -u +%s)
  CERT=$(python3 -c "
import json
led=json.load(open('final_deck_ledger.json'))
print(sum(1 for p in led['pages'] if p['status']=='certified'))")
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) loop: certified=$CERT/37 elapsed=$((NOW-START))s" >> pool_run/hygiene2.log
  if [ "$CERT" -ge 37 ]; then
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) ALL 37 CERTIFIED — loop exiting" >> pool_run/hygiene2.log
    break
  fi
  if [ $((NOW-START)) -ge $BUDGET ]; then
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) 2h budget exhausted — loop exiting" >> pool_run/hygiene2.log
    break
  fi
  sleep 90
done
