#!/usr/bin/env bash
# fresh2_status.sh — poll fresh2 leg transcripts + carrier liveness for slides 045-051.
set -u
ROOT=/home/codespace/ai_llm_slides
NS=$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
verd() { [ -f "$1" ] && grep -oE 'FINAL VERDICT: *\*{0,2} *(PASS|FAIL)' "$1" | tail -1 || echo "none"; }
r429() { [ -f "$1" ] && grep -ci 429 "$1" || echo 0; }
for N in 045 046 047 049 050 051; do
  D=$RJ/slide$N
  F=$D/judge_full_fresh2.txt; C=$D/crop_dense_judge_fresh2.txt
  FP=$(cat $RJ/legs_20261031.pids/${N}_full_fresh2.pid 2>/dev/null); CP=$(cat $RJ/legs_20261031.pids/${N}_crop_fresh2.pid 2>/dev/null)
  FA=y; kill -0 "$FP" 2>/dev/null || FA=n; CA=y; kill -0 "$CP" 2>/dev/null || CA=n
  echo "$N FULL[$FA pid=$FP]: $(verd $F) 429=$(r429 $F) | CROP[$CA pid=$CP]: $(verd $C) 429=$(r429 $C)"
done
echo "occ=$(pgrep -c -f analyze_image.py) legs=$(pgrep -c -f vision_leg.sh) $(date -u +%FT%TZ)"
