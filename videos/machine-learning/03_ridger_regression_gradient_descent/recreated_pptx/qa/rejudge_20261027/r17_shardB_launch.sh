#!/usr/bin/env bash
# r17 shard B launcher — slides 018-034 (skip 025, 033 fix-owned).
# Targets: $D/judge_full_r17.txt (t=1200, payload_A.txt) and $D/crop_dense_judge_r17.txt
# (t=600, payload_B_NNN.txt). Launch only when no live vision_leg.sh wrapper owns the
# r17 target. ALWAYS OCC_MAX=700 + setsid nohup, detached.
set -u
ROOT=/home/codespace/ai_llm_slides
NS=$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
LOG=$RJ/r17_shardB_launch.log
PIDDIR=$RJ/legs_20261031.pids
mkdir -p "$PIDDIR"
: > "$LOG"

clean() { [ -f "$1" ] && grep -q 'FINAL VERDICT' "$1" 2>/dev/null && ! grep -qi '429' "$1" 2>/dev/null; }
owned() { ps -eo args | grep '[v]ision_leg.sh' | grep -q "$1"; }

for N in 018 019 020 021 022 023 024 026 027 028 029 030 031 032 034; do
  D=$RJ/slide$N; NN=$((10#$N))
  # full leg
  T=$D/judge_full_r17.txt
  if clean "$T"; then
    echo "$N full: clean r17 transcript already banked, skip" >> "$LOG"
  elif owned "slide$N/judge_full_r17.txt"; then
    echo "$N full: live wrapper owns r17 target, skip" >> "$LOG"
  else
    OCC_MAX=700 setsid nohup bash "$RJ/vision_leg.sh" "$T" 1200 \
      "$D/render.png" "$NS/unique_slides/slide_${N}.jpg" \
      "Slide $NN recreation — fidelity check vs original lecture frame (r17)" \
      "IMG1=150dpi PNG render of 13.33x7.5in PPTX; IMG2=original 960x540 lecture frame" \
      "$RJ/payload_A.txt" > "$D/judge_full_r17.wrapper.out" 2>&1 < /dev/null &
    echo $! > "$PIDDIR/${N}_r17_full.pid"
    echo "$N full launched pid $! -> judge_full_r17.txt" >> "$LOG"
  fi
  # crop leg
  T=$D/crop_dense_judge_r17.txt
  if clean "$T"; then
    echo "$N crop: clean r17 transcript already banked, skip" >> "$LOG"
  elif owned "slide$N/crop_dense_judge_r17.txt"; then
    echo "$N crop: live wrapper owns r17 target, skip" >> "$LOG"
  else
    if ! { [ -f "$D/crop_dense_render.png" ] && [ -f "$D/crop_dense_orig.png" ]; }; then
      echo "$N crop: pair missing, running pick_dense_region.py $N" >> "$LOG"
      python3 "$RJ/pick_dense_region.py" "$N" >> "$LOG" 2>&1
    fi
    OCC_MAX=700 setsid nohup bash "$RJ/vision_leg.sh" "$T" 600 \
      "$D/crop_dense_render.png" "$D/crop_dense_orig.png" \
      "Slide $NN zoomed crop — fidelity check vs original (r17)" \
      "IMG1=zoomed crop of 150dpi render; IMG2=matched-scale crop of original frame" \
      "$RJ/payload_B_${N}.txt" > "$D/crop_dense_judge_r17.wrapper.out" 2>&1 < /dev/null &
    echo $! > "$PIDDIR/${N}_r17_crop.pid"
    echo "$N crop launched pid $! -> crop_dense_judge_r17.txt" >> "$LOG"
  fi
done
echo "LAUNCH_DONE $(date -u +%FT%TZ)" >> "$LOG"
cat "$LOG"
