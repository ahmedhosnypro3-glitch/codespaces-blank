#!/usr/bin/env bash
# Serial queue of detached parse-verification cross-checks (gateway-friendly: one at a time).
set -u
V=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/analysis/parse/adjudication/vision
for N in 012 011 009 010 007; do
  if [ -s "$V/slide_$N.vision.txt" ]; then
    echo "SKIP_$N (already banked)" >> "$V/run_status.log"
    continue
  fi
  bash "$V/run_one.sh" "$N" "$V/p$N.txt" >> "$V/run_status.log" 2>&1
done
echo "QUEUE_DONE" >> "$V/run_status.log"
