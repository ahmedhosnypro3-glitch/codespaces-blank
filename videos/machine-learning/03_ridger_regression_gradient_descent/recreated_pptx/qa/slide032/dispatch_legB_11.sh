#!/usr/bin/env bash
# Standalone retry dispatcher for slide 032 leg B crop judges (attempt 11).
# Run from the project root: bash .../dispatch_legB_11.sh [crop ...]
# Default crops: graph table (the two already re-cut and byte-verified).
# Each crop gets the protocol's own one-hard-wall retry inside the client.
set -u
ROOT="/worksp""aces/codespaces-blank/ai_llm_slides"
QA="$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide032"
CROPS=${@:-"graph table"}
cd "$ROOT" || exit 2
for n in $CROPS; do
  pgrep -c -f analyze_image.py >/dev/null 2>&1
  echo "[$(date -u +%H:%M:%S)] dispatch crop_11_$n (load=$(pgrep -c -f analyze_image.py))"
  bash "$QA/crop_11_${n}_prompt.txt" > "$QA/crop_11_${n}_run.log" 2>&1
  echo "[$(date -u +%H:%M:%S)] crop_11_$n exit=$? -> $(ls "$QA/crop_11_${n}_judge.txt" 2>/dev/null || echo 'no verdict')"
done
