#!/usr/bin/env bash
# Serial retry queue of detached parse-verification cross-checks (one at a time).
set -u
V=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/analysis/parse/adjudication/vision
mkdir -p "$V/prior_attempts"
for N in 007 008 009 010 011; do
  bash "$V/run_one2.sh" "$N" "$V/p$N.txt" >> "$V/run_status2.log" 2>&1
done
echo "QUEUE2_DONE" >> "$V/run_status2.log"
