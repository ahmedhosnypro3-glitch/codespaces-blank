#!/usr/bin/env bash
# r21 shard A gap-fill launcher (2026-10-31, HARVEST10 wave) — slides missing a
# fresh (post 2026-10-31 03:00 UTC) clean FULL and/or CROP verdict:
#   009 crop, 010 full+crop, 011 full, 016 full+crop.
# Targets: $D/judge_full_r21.txt (t=1200, payload_A.txt) and
#          $D/crop_dense_judge_r21.txt (t=600, payload_B_NNN.txt).
# Launch only when no live vision_leg.sh wrapper owns the r21 target.
# ALWAYS OCC_MAX=700 + setsid nohup, detached. Never touches 014/019/025/033/050/051.
set -u
ROOT=/home/codespace/ai_llm_slides
NS=$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
LOG=$RJ/r21_shardA_launch.log
PIDDIR=$RJ/legs_20261031.pids
mkdir -p "$PIDDIR"
: > "$LOG"

clean() { [ -f "$1" ] && grep -q 'FINAL VERDICT' "$1" 2>/dev/null && ! grep -qi '429' "$1" 2>/dev/null; }
fresh() { # clean AND newer than 2026-10-31 03:00 UTC
  [ -f "$1" ] || return 1
  local mt; mt=$(stat -c %Y "$1" 2>/dev/null) || return 1
  [ "$mt" -gt 1793415600 ] || return 1
  clean "$1"
}
owned() { ps -eo args | grep '[v]ision_leg.sh' | grep -q "$1"; }

launch_full() { # N
  local N=$1
  local D=$RJ/slide$N NN=$((10#$N)) T=$RJ/slide$N/judge_full_r21.txt
  if fresh "$T"; then echo "$N full: fresh clean r21 already banked, skip" >> "$LOG"; return; fi
  if owned "slide$N/judge_full_r21.txt"; then echo "$N full: live wrapper owns r21 target, skip" >> "$LOG"; return; fi
  OCC_MAX=700 setsid nohup bash "$RJ/vision_leg.sh" "$T" 1200 \
    "$D/render.png" "$NS/unique_slides/slide_${N}.jpg" \
    "Slide $NN recreation — fidelity check vs original (r21)" \
    "IMG1=150dpi render; IMG2=original frame" \
    "$RJ/payload_A.txt" > "$D/judge_full_r21.wrapper.out" 2>&1 < /dev/null &
  echo $! > "$PIDDIR/${N}_r21_full.pid"
  echo "$N full launched pid $! -> judge_full_r21.txt" >> "$LOG"
}

launch_crop() { # N
  local N=$1
  local D=$RJ/slide$N NN=$((10#$N)) T=$RJ/slide$N/crop_dense_judge_r21.txt
  if fresh "$T"; then echo "$N crop: fresh clean r21 already banked, skip" >> "$LOG"; return; fi
  if owned "slide$N/crop_dense_judge_r21.txt"; then echo "$N crop: live wrapper owns r21 target, skip" >> "$LOG"; return; fi
  if ! { [ -f "$D/crop_dense_render.png" ] && [ -f "$D/crop_dense_orig.png" ]; }; then
    echo "$N crop: pair missing, running pick_dense_region.py $N" >> "$LOG"
    (cd "$ROOT" && python3 "$RJ/pick_dense_region.py" "$N") >> "$LOG" 2>&1
  fi
  OCC_MAX=700 setsid nohup bash "$RJ/vision_leg.sh" "$T" 600 \
    "$D/crop_dense_render.png" "$D/crop_dense_orig.png" \
    "Slide $NN zoomed crop — fidelity check vs original (r21)" \
    "IMG1=zoomed crop of 150dpi render; IMG2=matched-scale crop of original frame" \
    "$RJ/payload_B_${N}.txt" > "$D/crop_dense_judge_r21.wrapper.out" 2>&1 < /dev/null &
  echo $! > "$PIDDIR/${N}_r21_crop.pid"
  echo "$N crop launched pid $! -> crop_dense_judge_r21.txt" >> "$LOG"
}

launch_crop 009
launch_full 010; launch_crop 010
launch_full 011
launch_full 016; launch_crop 016
echo "LAUNCH_DONE $(date -u +%FT%TZ)" >> "$LOG"
cat "$LOG"
