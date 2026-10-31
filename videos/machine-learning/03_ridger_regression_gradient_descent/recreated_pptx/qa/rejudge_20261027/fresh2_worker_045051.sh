#!/usr/bin/env bash
# fresh2_worker_045051.sh — FRESH worker spawn 2026-10-31 ~03:0x: fill missing rejudge
# legs for slides 045 046 047 049 050 051 (skip 25; 043/044/048 done; 035-042 done).
# Transcript names use *_fresh2.txt so in-flight foreign carriers writing
# judge_full.txt / crop_dense_judge.txt are never clobbered (vision_leg.sh rm -f's OUT).
set -u
ROOT=/home/codespace/ai_llm_slides
NS=$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
export TMPDIR=$ROOT/scratch/tmp
mkdir -p "$TMPDIR" "$RJ/legs_20261031.pids"
cd "$ROOT"

for N in 045 046 047 049 050 051; do
  D=$RJ/slide$N
  NN=$((10#$N))
  for f in render.png crop_dense_render.png crop_dense_orig.png; do
    [ -f "$D/$f" ] || { echo "MISSING $N $f"; exit 2; }
  done
  [ -f "$RJ/payload_B_$N.txt" ] || { echo "MISSING payload_B_$N"; exit 2; }

  # skip a leg if a clean (FINAL VERDICT, no 429) fresh2 transcript already exists
  if [ -f "$D/judge_full_fresh2.txt" ] && grep -q 'FINAL VERDICT' "$D/judge_full_fresh2.txt" && ! grep -qi '429' "$D/judge_full_fresh2.txt"; then
    echo "$N full already banked fresh2"
  else
    setsid nohup bash "$RJ/vision_leg.sh" "$D/judge_full_fresh2.txt" 1200 \
      "$D/render.png" "$NS/unique_slides/slide_$N.jpg" \
      "Slide $NN recreation — fidelity check vs original lecture frame" \
      "IMG1=150dpi PNG render of 13.33x7.5in PPTX; IMG2=original 960x540 lecture frame" \
      "$RJ/payload_A.txt" > "$D/judge_full_fresh2.txt.wrapper.out" 2>&1 &
    echo $! > "$RJ/legs_20261031.pids/${N}_full_fresh2.pid"
    echo "launched $N FULL  pid $! -> judge_full_fresh2.txt"
  fi

  if [ -f "$D/crop_dense_judge_fresh2.txt" ] && grep -q 'FINAL VERDICT' "$D/crop_dense_judge_fresh2.txt" && ! grep -qi '429' "$D/crop_dense_judge_fresh2.txt"; then
    echo "$N crop already banked fresh2"
  else
    setsid nohup bash "$RJ/vision_leg.sh" "$D/crop_dense_judge_fresh2.txt" 600 \
      "$D/crop_dense_render.png" "$D/crop_dense_orig.png" \
      "Slide $NN zoomed crop — fidelity check vs original" \
      "IMG1=zoomed crop of 150dpi render; IMG2=matched-scale crop of original frame" \
      "$RJ/payload_B_$N.txt" > "$D/crop_dense_judge_fresh2.txt.wrapper.out" 2>&1 &
    echo $! > "$RJ/legs_20261031.pids/${N}_crop_fresh2.pid"
    echo "launched $N CROP  pid $! -> crop_dense_judge_fresh2.txt"
  fi
done
echo "FRESH2_DISPATCH_DONE $(date -u +%FT%TZ)"
