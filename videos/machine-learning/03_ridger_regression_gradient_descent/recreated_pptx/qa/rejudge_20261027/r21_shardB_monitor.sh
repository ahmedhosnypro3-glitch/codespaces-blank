#!/usr/bin/env bash
RJ=/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/rejudge_20261027
M=$RJ/r21_shardB_monitor.log
: > "$M"
for i in $(seq 1 22); do
  echo "=== POLL $i $(date -u +%FT%TZ) ===" >> "$M"
  bash "$RJ/r21_shardB_status.sh" >> "$M" 2>&1
  sleep 280
done
echo "MONITOR_DONE $(date -u +%FT%TZ)" >> "$M"
