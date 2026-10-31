#!/usr/bin/env bash
# waveW4_launch_001017.sh — wave W4 fresh rejudge legs for slides 001..017 of
# deck 03, on current certified pptx bytes. Renders render_w4.png (150dpi,
# unique LO profile per slide under scratch/tmp), builds the w4 crop pair via
# pick_dense_region.py + PIL recipe from fresh_leg_chain.sh, then launches
# full (payload_A) + crop (payload_B_025) vision legs as durable
# setsid-nohup wrappers, 2 slides (4 legs) at a time, each bash call ending
# with wait. Never touches the DB, never modifies pptx files, never deletes
# banked evidence. Appends only to waveW4_*.log/md5 in $RJ.
set -u
ROOT=/home/codespace/ai_llm_slides
cd "$ROOT" || exit 1
NS=videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
export TMPDIR=$ROOT/scratch/tmp
mkdir -p "$TMPDIR"
LOG=$RJ/waveW4_launch_001017.log
exec >> "$LOG" 2>&1
echo "=== waveW4 launch 001-017 start $(date -u +%FT%TZ) pid=$$"

clean() { # transcript -> PASS|FAIL|NORESULT (clean = FINAL VERDICT present, no 429)
  local f=$1
  [ -f "$f" ] || { echo NORESULT; return; }
  grep -q 'FINAL VERDICT' "$f" && ! grep -qi '429' "$f" || { echo NORESULT; return; }
  grep -oE 'FINAL VERDICT: *\*{0,2} *(PASS|FAIL)' "$f" | tail -1 | grep -oE '(PASS|FAIL)'
}

render_slide() {
  local n=$1 d=$RJ/slide$n pptx=$NS/recreated_pptx/slide_${n}_recreated.pptx
  mkdir -p "$d" "$d/w4"
  echo "$(date -u +%FT%TZ) slide_$n $(md5sum "$pptx")" >> "$RJ/waveW4_md5_001017.txt"
  if [ -f "$d/render_w4.png" ] && [ "$d/render_w4.png" -nt "$pptx" ]; then
    echo "$n render_w4.png fresh: $(python3 -c "from PIL import Image;print(Image.open('$d/render_w4.png').size)")"
    return
  fi
  echo "$n rendering w4 $(date -u +%FT%TZ)"
  rm -f "$d"/w4/slide_${n}_recreated.pdf "$d/render_w4.png"
  soffice --headless "-env:UserInstallation=file://$TMPDIR/lo_w4_$n" \
    --convert-to pdf "$pptx" --outdir "$d/w4" > "$d/w4/render_w4_soffice.log" 2>&1
  pdftoppm -png -r 150 -singlefile "$d/w4/slide_${n}_recreated.pdf" "$d/render_w4" >> "$d/w4/render_w4_soffice.log" 2>&1
  echo "$n render_w4.png = $(python3 -c "from PIL import Image;print(Image.open('$d/render_w4.png').size)" 2>/dev/null) $(date -u +%FT%TZ)"
}

crop_slide() {
  local n=$1 d=$RJ/slide$n
  if [ -f "$d/crop_dense_render_w4.png" ] && [ -f "$d/crop_dense_orig_w4.png" ] && \
     [ "$d/crop_dense_render_w4.png" -nt "$d/render_w4.png" ]; then
    echo "$n w4 crop pair fresh"; return
  fi
  read -r X0 Y0 X1 Y1 < <(python3 "$RJ/pick_dense_region.py" "$n")
  echo "$n w4 crop region $X0 $Y0 $X1 $Y1"
  python3 - "$d/render_w4.png" "$NS/unique_slides/slide_$n.jpg" "$d" "$X0" "$Y0" "$X1" "$Y1" <<'PY'
import sys
import numpy as np
from PIL import Image
rp, op, out, x0, y0, x1, y1 = sys.argv[1], sys.argv[2], sys.argv[3], *map(int, sys.argv[4:8])
r = Image.open(rp).convert("RGB"); o = Image.open(op).convert("RGB")
sc = r.size[1] / 540.0
rc = r.crop((int(x0*sc), int(y0*sc), int(np.ceil(x1*sc)), int(np.ceil(y1*sc))))
oc = o.crop((x0, y0, x1, y1)).resize(rc.size, Image.LANCZOS)
rc.save(f"{out}/crop_dense_render_w4.png"); oc.save(f"{out}/crop_dense_orig_w4.png")
PY
  echo "$n w4 crops render=$(python3 -c "from PIL import Image;print(Image.open('$d/crop_dense_render_w4.png').size)") orig=$(python3 -c "from PIL import Image;print(Image.open('$d/crop_dense_orig_w4.png').size)")"
}

launch_pair() {
  local pids=() n d
  for n in "$@"; do
    d=$RJ/slide$n
    if [ -f "$d/judge_full_w4.txt" ] && grep -q 'FINAL VERDICT' "$d/judge_full_w4.txt" && ! grep -qi '429' "$d/judge_full_w4.txt"; then
      echo "$n SKIP: judge_full_w4.txt already clean verdict=$(clean "$d/judge_full_w4.txt") $(date -u +%FT%TZ)"
      continue
    fi
    render_slide "$n"
    crop_slide "$n"
    OCC_MAX=700 ATTEMPTS=10 setsid nohup bash "$RJ/vision_leg.sh" \
      "$d/judge_full_w4.txt" 600 "$d/render_w4.png" "$NS/unique_slides/slide_$n.jpg" \
      "Slide $n full — rejudge 2026-10-27 wave W4" \
      "2001x1125 CSS 960x540 scale, app render" \
      "$RJ/payload_A.txt" > "$d/judge_full_w4.wrapper.out" 2>&1 < /dev/null &
    pids+=($!)
    OCC_MAX=700 ATTEMPTS=10 setsid nohup bash "$RJ/vision_leg.sh" \
      "$d/judge_crop_w4.txt" 600 "$d/crop_dense_render_w4.png" "$d/crop_dense_orig_w4.png" \
      "Slide $n crop — rejudge 2026-10-27 wave W4" \
      "matched-scale dense-region crop pair (960x540 frame coords), app render vs original" \
      "$RJ/payload_B_025.txt" > "$d/judge_crop_w4.wrapper.out" 2>&1 < /dev/null &
    pids+=($!)
    echo "$n legs launched: full pid=${pids[$(( ${#pids[@]} - 2 ))]} crop pid=${pids[$(( ${#pids[@]} - 1 ))]} $(date -u +%FT%TZ)"
  done
  if [ ${#pids[@]} -gt 0 ]; then wait "${pids[@]}"; fi
  # safeguard: no w4 leg wrapper may survive into the next pair (2-slide wall)
  local i
  for i in $(seq 1 120); do
    pgrep -f "vision_leg\.sh .*judge_.*_w4\.txt" > /dev/null || break
    sleep 30
  done
  for n in "$@"; do
    d=$RJ/slide$n
    echo "$n pair DONE full=$(clean "$d/judge_full_w4.txt") crop=$(clean "$d/judge_crop_w4.txt") $(date -u +%FT%TZ)"
  done
}

for batch in "001 002 003 004" "005 006 007 008" "009 010 011 012" "013 014 015 016" "017"; do
  set -- $batch
  echo "=== batch [$batch] start $(date -u +%FT%TZ)"
  launch_pair "$1" "$2"
  if [ $# -ge 4 ]; then launch_pair "$3" "$4"; fi
done
echo "=== waveW4 launch 001-017 ALL DONE $(date -u +%FT%TZ)"
