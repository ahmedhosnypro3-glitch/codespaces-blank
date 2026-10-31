#!/usr/bin/env bash
# w5_batch.sh NNN NNN — wave W5 fresh FULL+CROP vision legs for a batch of 2 slides.
# Per slide: md5sum pptx, render to render_w5.png if missing/stale, crop pair
# (crop_dense_render_w5.png / crop_dense_orig_w5.png), launch both legs with
# durable wrappers, wait. Never touches DB or pptx. Appends register lines.
set -u
ROOT=/home/codespace/ai_llm_slides
cd "$ROOT" || exit 1
NS=videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
ANS=$ROOT/$NS
export TMPDIR=$ROOT/scratch/tmp
mkdir -p "$TMPDIR"

clean() { # transcript -> PASS|FAIL|NORESULT (clean = FINAL VERDICT and no 429)
  local f=$1
  [ -f "$f" ] || { echo NORESULT; return; }
  grep -q 'FINAL VERDICT' "$f" && ! grep -qi '429' "$f" || { echo NORESULT; return; }
  grep -oE 'FINAL VERDICT: *\*{0,2} *(PASS|FAIL)' "$f" | tail -1 | grep -oE '(PASS|FAIL)'
}

prep() { # NNN -> renders + crop pair; echoes md5
  local N=$1 D=$RJ/slide$N PPTX=$ANS/recreated_pptx/slide_${N}_recreated.pptx
  mkdir -p "$D"
  local MD5; MD5=$(md5sum "$PPTX" | cut -d' ' -f1)
  echo "$MD5" > "$D/w5_pptx.md5"
  if [ ! -f "$D/render_w5.png" ] || [ "$PPTX" -nt "$D/render_w5.png" ]; then
    echo "--- $N render (md5=$MD5) $(date -u +%FT%TZ)"
    rm -f "$D/slide_${N}_recreated.pdf"
    soffice --headless "-env:UserInstallation=file://$TMPDIR/lo_w5_${N}" \
      --convert-to pdf "$PPTX" --outdir "$D" > "$D/render_w5.log" 2>&1
    pdftoppm -png -r 150 -singlefile "$D/slide_${N}_recreated.pdf" "$D/render_w5" >> "$D/render_w5.log" 2>&1
  else
    echo "--- $N render_w5.png fresh, reuse (md5=$MD5)"
  fi
  if [ ! -f "$D/crop_dense_render_w5.png" ] || [ ! -f "$D/crop_dense_orig_w5.png" ] \
     || [ "$D/render_w5.png" -nt "$D/crop_dense_render_w5.png" ]; then
    read -r X0 Y0 X1 Y1 < <(python3 "$RJ/pick_dense_region.py" "$N")
    echo "--- $N crop region $X0 $Y0 $X1 $Y1"
    python3 - "$D/render_w5.png" "$ANS/unique_slides/slide_${N}.jpg" "$D" "$X0" "$Y0" "$X1" "$Y1" <<'PY'
import sys
import numpy as np
from PIL import Image
rp, op, out, x0, y0, x1, y1 = sys.argv[1], sys.argv[2], sys.argv[3], *map(int, sys.argv[4:8])
r = Image.open(rp).convert("RGB"); o = Image.open(op).convert("RGB")
sc = r.size[1] / 540.0
rc = r.crop((int(x0*sc), int(y0*sc), int(np.ceil(x1*sc)), int(np.ceil(y1*sc))))
oc = o.crop((x0, y0, x1, y1)).resize(rc.size, Image.LANCZOS)
rc.save(f"{out}/crop_dense_render_w5.png"); oc.save(f"{out}/crop_dense_orig_w5.png")
PY
  fi
  echo "$MD5"
}

for N in "$@"; do
  D=$RJ/slide$N
  MD5=$(prep "$N")
  echo "--- $N launching W5 legs $(date -u +%FT%TZ)"
  OCC_MAX=700 ATTEMPTS=10 setsid nohup bash "$ROOT/$RJ/vision_leg.sh" \
    "$ROOT/$RJ/slide$N/judge_full_w5.txt" 600 "$ROOT/$RJ/slide$N/render_w5.png" \
    "$ANS/unique_slides/slide_${N}.jpg" \
    "Slide $N full — rejudge wave W5" "2001x1125, app render" \
    "$ROOT/$RJ/payload_A.txt" > "$D/judge_full_w5.wrapper.out" 2>&1 &
  OCC_MAX=700 ATTEMPTS=10 setsid nohup bash "$ROOT/$RJ/vision_leg.sh" \
    "$ROOT/$RJ/slide$N/crop_dense_judge_w5.txt" 600 "$ROOT/$RJ/slide$N/crop_dense_render_w5.png" \
    "$ROOT/$RJ/slide$N/crop_dense_orig_w5.png" \
    "Slide $N crop — rejudge wave W5" "zoomed crop pair, matched scale" \
    "$ROOT/$RJ/payload_B_025.txt" > "$D/crop_dense_judge_w5.wrapper.out" 2>&1 &
done
wait
echo "=== batch $* legs finished $(date -u +%FT%TZ)"
for N in "$@"; do
  D=$RJ/slide$N
  FV=$(clean "$D/judge_full_w5.txt"); [ -z "$FV" ] && FV=NORESULT
  BV=$(clean "$D/crop_dense_judge_w5.txt"); [ -z "$BV" ] && BV=NORESULT
  MD5=$(cat "$D/w5_pptx.md5" 2>/dev/null)
  {
    echo ""
    echo "| $N | W5 | FULL=$FV | CROP=$BV | md5=$MD5 | legs judge_full_w5.txt + crop_dense_judge_w5.txt (payload_A / payload_B_025, OCC_MAX=700 ATTEMPTS=10) $(date -u +%FT%TZ) |"
  } >> "$RJ/REJUDGE_REGISTER.md"
  echo "slide $N FULL=$FV CROP=$BV md5=$MD5"
done
echo "=== batch $* DONE $(date -u +%FT%TZ)"
