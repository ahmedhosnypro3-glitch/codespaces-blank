#!/usr/bin/env bash
# r17 shard C launcher — slides 035-051 (025 out of shard range, skipped).
# Targets: $D/judge_full_r17.txt (t=1200, payload_A.txt vs unique_slides/slide_NNN.jpg)
# and $D/crop_dense_judge_r17.txt (t=600, payload_B_NNN.txt over the dense crop pair).
# Slide 050 special: crop_dense_judge_fresh4.txt missing/unclean -> the r17 crop target
# IS the relaunch (crop_dense_judge_r17.txt).
# Launch only when no live vision_leg.sh wrapper owns the r17 target.
# ALWAYS OCC_MAX=700 + setsid nohup, detached.
set -u
ROOT=/home/codespace/ai_llm_slides
NS=$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
LOG=$RJ/r17_shardC_launch.log
: > "$LOG"
mkdir -p "$RJ/legs_20261031.pids"

clean() { [ -f "$1" ] && grep -q 'FINAL VERDICT' "$1" 2>/dev/null && ! grep -qi '429' "$1" 2>/dev/null; }
owned() { ps -eo args | grep '[v]ision_leg.sh' | grep -q "$1"; }

for N in 035 036 037 038 039 040 041 042 043 044 045 046 047 048 049 050 051; do
  D=$RJ/slide$N; NN=$((10#$N))
  # full leg
  T=$D/judge_full_r17.txt
  if clean "$T"; then
    echo "$N full: clean r17 transcript already banked, skip" >> "$LOG"
  elif owned "slide$N/judge_full_r17.txt"; then
    echo "$N full: live wrapper owns r17 target, skip" >> "$LOG"
  else
    [ -f "$D/render.png" ] || { echo "$N full: render.png missing, skip" >> "$LOG"; continue; }
    OCC_MAX=700 setsid nohup bash "$RJ/vision_leg.sh" "$T" 1200 \
      "$D/render.png" "$NS/unique_slides/slide_${N}.jpg" \
      "Slide $NN recreation — fidelity check vs original lecture frame" \
      "IMG1=150dpi PNG render of 13.33x7.5in PPTX; IMG2=original 960x540 lecture frame" \
      "$RJ/payload_A.txt" > "$D/judge_full_r17.wrapper.out" 2>&1 < /dev/null &
    echo $! > "$RJ/legs_20261031.pids/${N}_r17_full.pid"
    echo "$N full launched pid $! -> judge_full_r17.txt" >> "$LOG"
  fi
  # crop leg
  T=$D/crop_dense_judge_r17.txt
  if clean "$T"; then
    echo "$N crop: clean r17 transcript already banked, skip" >> "$LOG"
  elif owned "slide$N/crop_dense_judge_r17.txt"; then
    echo "$N crop: live wrapper owns r17 target, skip" >> "$LOG"
  else
    if [ ! -f "$D/crop_dense_render.png" ] || [ ! -f "$D/crop_dense_orig.png" ]; then
      echo "$N crop: pair missing, regenerating via pick_dense_region.py" >> "$LOG"
      read -r X0 Y0 X1 Y1 < <(cd "$ROOT" && python3 "$RJ/pick_dense_region.py" "$N") || { echo "$N crop: pick_dense_region failed, skip" >> "$LOG"; continue; }
      (cd "$ROOT" && python3 - "$D/render.png" "$NS/unique_slides/slide_$N.jpg" "$D" "$X0" "$Y0" "$X1" "$Y1" <<'PY'
import sys
import numpy as np
from PIL import Image
rp, op, out, x0, y0, x1, y1 = sys.argv[1], sys.argv[2], sys.argv[3], *map(int, sys.argv[4:8])
r = Image.open(rp).convert("RGB")
o = Image.open(op).convert("RGB")
sc = r.size[1] / 540.0
rc = r.crop((int(x0 * sc), int(y0 * sc), int(np.ceil(x1 * sc)), int(np.ceil(y1 * sc))))
oc = o.crop((x0, y0, x1, y1)).resize(rc.size, Image.LANCZOS)
rc.save(f"{out}/crop_dense_render.png")
oc.save(f"{out}/crop_dense_orig.png")
print("crop pair rebuilt", rc.size)
PY
) >> "$LOG" 2>&1
    fi
    [ -f "$D/crop_dense_render.png" ] && [ -f "$D/crop_dense_orig.png" ] || { echo "$N crop: pair still missing, skip" >> "$LOG"; continue; }
    NOTE=""
    if [ "$N" = "050" ]; then
      if clean "$D/crop_dense_judge_fresh4.txt"; then NOTE="fresh4 clean"; else NOTE="fresh4 missing/unclean -> r17 is the relaunch"; fi
      echo "$N crop: $NOTE" >> "$LOG"
    fi
    OCC_MAX=700 setsid nohup bash "$RJ/vision_leg.sh" "$T" 600 \
      "$D/crop_dense_render.png" "$D/crop_dense_orig.png" \
      "Slide $NN zoomed crop — fidelity check vs original" \
      "IMG1=zoomed crop of 150dpi render; IMG2=matched-scale crop of original frame" \
      "$RJ/payload_B_${N}.txt" > "$D/crop_dense_judge_r17.wrapper.out" 2>&1 < /dev/null &
    echo $! > "$RJ/legs_20261031.pids/${N}_r17_crop.pid"
    echo "$N crop launched pid $! -> crop_dense_judge_r17.txt" >> "$LOG"
  fi
done
echo "LAUNCH_DONE $(date -u +%FT%TZ)" >> "$LOG"
cat "$LOG"
