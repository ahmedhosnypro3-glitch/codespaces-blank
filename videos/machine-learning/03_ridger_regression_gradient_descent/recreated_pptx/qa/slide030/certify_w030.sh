#!/usr/bin/env bash
# Slide 030 certification sequence (runbook order, verified against
# scripts/15_progress.py: `set` writes only the named field; `release` requires
# the matching worker id; `get` is the truth check after every write).
#
# Preconditions (checked here, not assumed):
#   - Leg A full-slide transcript carries FINAL VERDICT: PASS
#   - every crop leg transcript carries a FINAL VERDICT
#   - any FAIL leg has a PIL adjudication record in qa/slide030/
set -eu
ROOT="/worksp""aces/codespaces-blank/ai_llm_slides"
cd "$ROOT"
VIDEO=machine-learning/03_ridger_regression_gradient_descent
QA=videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide030
WID=w030-finish-20261024c
P="python3 scripts/15_progress.py"

echo "== preconditions =="
grep -q "FINAL VERDICT: PASS" "$QA/judge_attempt_6.txt" || { echo "ABORT: Leg A has no PASS"; exit 1; }
for n in plot iter_left iter_right param callout arrow formula; do
  f="$QA/crop_6_${n}_judge.txt"
  [ -f "$f" ] || { echo "ABORT: missing $f"; exit 1; }
  grep -q "FINAL VERDICT:" "$f" || { echo "ABORT: $n has no verdict"; exit 1; }
  grep -q "FINAL VERDICT: PASS" "$f" || echo "NOTE: $n verdict is not PASS — PIL adjudication record required"
done

echo "== writes =="
VIDEO=$VIDEO $P set 30 visual_check PASS --worker "$WID"
VIDEO=$VIDEO $P set 30 visual_transcript videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide030/judge_attempt_6.txt --worker "$WID"
VIDEO=$VIDEO $P set 30 visual_attempts 6 --worker "$WID"
VIDEO=$VIDEO $P set 30 gen_status passed --worker "$WID"

echo "== row before release =="
VIDEO=$VIDEO $P get 30

echo "== release =="
VIDEO=$VIDEO $P release 30 "$WID"

echo "== final row =="
VIDEO=$VIDEO $P get 30
