#!/usr/bin/env bash
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
cd "$NS" || exit 1
LOG="$NS/_pool/wlogs/b05_reanalysis9_resilient.log"
for cycle in 1 2 3 4; do
  echo "cycle $cycle start $(date +%T)" >> "$LOG"
  TMPDIR="$NS/_pool" python3 /home/codespace/ai_llm_slides/scripts/12_analyze_slides.py \
    unique_slides analysis/reanalysis --slides 9 >> "$LOG" 2>&1
  if [ -f analysis/reanalysis/slide_009_raw.json ]; then
    TMPDIR="$NS/_pool" python3 /home/codespace/ai_llm_slides/scripts/13_validate_slides.py \
      analysis/reanalysis --slides 9 >> "$LOG" 2>&1
    if [ -f analysis/reanalysis/slide_009_final.json ]; then
      echo "REANALYSIS OK cycle $cycle $(date +%T)" >> "$LOG"; exit 0
    fi
  fi
  echo "cycle $cycle failed $(date +%T)" >> "$LOG"; sleep 150
done
echo "EXHAUSTED $(date +%T)" >> "$LOG"
