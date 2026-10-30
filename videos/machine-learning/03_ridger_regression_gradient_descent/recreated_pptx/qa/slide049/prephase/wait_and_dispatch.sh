#!/bin/bash
# Gate-wait wrapper: dispatch ONE prephase leg when the fleet drops below 8.
# Retries ONLY gate-busy exits (75); a real vision failure propagates immediately.
# Usage: SLIDE_N=048 bash wait_and_dispatch.sh <leg>
set -u
cd /home/ahmed/Projects/ai_llm_slides || exit 3
n="${SLIDE_N:?}"; leg="${1:?}"
DIR="videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide$n/prephase"
ATTEMPT=0
while :; do
  ATTEMPT=$((ATTEMPT+1))
  if [ "$ATTEMPT" -gt 40 ]; then echo "GATE NEVER OPENED after $ATTEMPT probes — parking"; exit 9; fi
  out=$(SLIDE_N="$n" bash "$DIR/dispatch_orig_read.sh" "$leg" 2>&1)
  rc=$?
  echo "$out"
  if [ $rc -eq 75 ]; then echo "[wrap] gate busy, sleep 120 (attempt $ATTEMPT)"; sleep 120; continue; fi
  exit $rc
done
