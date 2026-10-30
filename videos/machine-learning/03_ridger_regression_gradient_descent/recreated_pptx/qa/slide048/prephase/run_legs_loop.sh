#!/bin/bash
# Relaunch the prephase leg chain after gate-starvation parks (rc 9), with backoff.
# Exits 0 only when run_legs.sh reports ALL LEGS BANKED; exits 8 on a real leg failure.
# Usage: SLIDE_N=048 bash run_legs_loop.sh <leg> [<leg> ...]
set -u
cd /home/ahmed/Projects/ai_llm_slides || exit 3
n="${SLIDE_N:?SLIDE_N must be set}"
DIR="videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide$n/prephase"
CYCLES="${CYCLES:-10}"
BACKOFF="${BACKOFF:-600}"
c=0
while [ "$c" -lt "$CYCLES" ]; do
  c=$((c+1))
  echo "[loop $n] cycle $c start $(date -u +%H:%M:%S)"
  SLIDE_N="$n" bash "$DIR/run_legs.sh" "$@"
  rc=$?
  if [ "$rc" -eq 0 ]; then echo "[loop $n] ALL LEGS BANKED — done"; exit 0; fi
  if [ "$rc" -eq 8 ]; then echo "[loop $n] real leg failure (rc 8) — stop"; exit 8; fi
  echo "[loop $n] chain parked (rc $rc) — backoff ${BACKOFF}s"
  sleep "$BACKOFF"
done
echo "[loop $n] exhausted $CYCLES cycles — parking honestly"
exit 9
