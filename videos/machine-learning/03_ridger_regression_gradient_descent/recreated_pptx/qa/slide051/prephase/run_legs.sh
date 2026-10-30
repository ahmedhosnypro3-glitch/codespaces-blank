#!/bin/bash
# Sequentially run prephase legs for one slide through the gate-wait wrapper.
# Skips legs whose transcripts are already banked; fails loud on first failure.
# Usage: SLIDE_N=049 bash run_legs.sh <leg> [<leg> ...]
set -u
cd /home/ahmed/Projects/ai_llm_slides || exit 3
n="${SLIDE_N:?SLIDE_N must be set}"
DIR="videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide$n/prephase"
W="$DIR/wait_and_dispatch.sh"
J="$DIR/orig_judges"
[ $# -ge 1 ] || { echo "usage: run_legs.sh <leg> ..."; exit 2; }
for leg in "$@"; do
  if [ -s "$J/orig_$leg.txt" ]; then
    echo "[chain $n] $leg already banked, skip"
    continue
  fi
  echo "[chain $n] dispatch $leg at $(date -u +%H:%M:%S)"
  SLIDE_N="$n" bash "$W" "$leg"
  rc=$?
  if [ "$rc" -eq 9 ]; then
    echo "[chain $n] $leg: gate never opened (wrapper rc 9) — stop chain"
    exit 9
  fi
  if [ ! -s "$J/orig_$leg.txt" ]; then
    echo "[chain $n] $leg: FAILED (rc $rc, no transcript) — stop chain"
    exit 8
  fi
  echo "[chain $n] $leg banked"
  sleep 5
done
echo "[chain $n] ALL LEGS BANKED"
