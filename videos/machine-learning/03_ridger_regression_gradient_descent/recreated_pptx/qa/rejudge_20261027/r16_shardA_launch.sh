#!/usr/bin/env bash
# r16 shard A launcher — slides 001-017 (skip 014 fix-owned; 025 out of shard).
# Targets: $D/judge_full_r16.txt (t=1200, payload_A.txt) and $D/crop_dense_judge_r16.txt
# (t=600, payload_B_NNN.txt). Launch only when no live vision_leg.sh wrapper owns the
# r16 target. ALWAYS OCC_MAX=700 + setsid nohup, detached.
set -u
ROOT=/home/codespace/ai_llm_slides
NS=$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
LOG=$RJ/r16_shardA_launch.log
: > "$LOG"

clean() { [ -f "$1" ] && grep -q 'FINAL VERDICT' "$1" 2>/dev/null && ! grep -qi '429' "$1" 2>/dev/null; }
owned() { ps -eo args | grep '[v]ision_leg.sh' | grep -q "$1"; }

for N in 001 002 003 004 005 006 007 008 009 010 011 012 013 015 016 017; do
  D=$RJ/slide$N; NN=$((10#$N))
  # full leg
  T=$D/judge_full_r16.txt
  if clean "$T"; then
    echo "$N full: clean r16 transcript already banked, skip" >> "$LOG"
  elif owned "slide$N/judge_full_r16.txt"; then
    echo "$N full: live wrapper owns r16 target, skip" >> "$LOG"
  else
    OCC_MAX=700 setsid nohup bash "$RJ/vision_leg.sh" "$T" 1200 \
      "$D/render.png" "$NS/unique_slides/slide_${N}.jpg" \
      "Slide $NN recreation — fidelity check vs original lecture frame" \
      "IMG1=150dpi PNG render of 13.33x7.5in PPTX; IMG2=original 960x540 lecture frame" \
      "$RJ/payload_A.txt" > "$D/judge_full_r16.wrapper.out" 2>&1 < /dev/null &
    echo $! > "$RJ/legs_20261031.pids/${N}_r16_full.pid"
    echo "$N full launched pid $! -> judge_full_r16.txt" >> "$LOG"
  fi
  # crop leg
  T=$D/crop_dense_judge_r16.txt
  if clean "$T"; then
    echo "$N crop: clean r16 transcript already banked, skip" >> "$LOG"
  elif owned "slide$N/crop_dense_judge_r16.txt"; then
    echo "$N crop: live wrapper owns r16 target, skip" >> "$LOG"
  else
    [ -f "$D/crop_dense_render.png" ] && [ -f "$D/crop_dense_orig.png" ] || { echo "$N crop: pair missing" >> "$LOG"; }
    OCC_MAX=700 setsid nohup bash "$RJ/vision_leg.sh" "$T" 600 \
      "$D/crop_dense_render.png" "$D/crop_dense_orig.png" \
      "Slide $NN zoomed crop — fidelity check vs original" \
      "IMG1=zoomed crop of 150dpi render; IMG2=matched-scale crop of original frame" \
      "$RJ/payload_B_${N}.txt" > "$D/crop_dense_judge_r16.wrapper.out" 2>&1 < /dev/null &
    echo $! > "$RJ/legs_20261031.pids/${N}_r16_crop.pid"
    echo "$N crop launched pid $! -> crop_dense_judge_r16.txt" >> "$LOG"
  fi
done
echo "LAUNCH_DONE $(date -u +%FT%TZ)" >> "$LOG"
cat "$LOG"
