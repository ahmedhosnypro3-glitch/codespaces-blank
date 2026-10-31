#!/bin/bash
# Certify-and-merge sweeper loop for 08_performance_measure (~40 min).
cd /home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure || exit 1
end=$((SECONDS + 2400))
while [ $SECONDS -lt $end ]; do
  out=$(python3 pool_run/sweeper_pm08_pass.py 2>&1)
  echo "$out"
  if echo "$out" | grep -q ALL37; then
    ts=$(date +%Y%m%dT%H%M%S)
    python3 pool_run/merge_final_deck.py gate 08-performance_final.pptx recreated_pptx 37 \
      > "pool_run/final_deck_gate_report_${ts}.txt" 2>&1
    rc=$?
    echo "GATE rc=$rc report=pool_run/final_deck_gate_report_${ts}.txt"
    cat "pool_run/final_deck_gate_report_${ts}.txt"
    break
  fi
  sleep 45
done
echo "LOOP EXIT after $((SECONDS))s"
