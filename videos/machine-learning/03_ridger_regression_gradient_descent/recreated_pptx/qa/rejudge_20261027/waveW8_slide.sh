#!/usr/bin/env bash
# waveW8_slide.sh N2 — one slide's W8 rejudge leg-pair for deck 03 (2026-10-31).
# usage: waveW8_slide.sh 03   (N2 = two-digit slide number; dirs slide03, slide05, ...)
# Steps: (1) render slide_NNN_recreated.pptx -> slideN2/render_w8.png (150dpi,
# unique LO profile lo_w8_N2 under scratch/tmp, pdftoppm -singlefile, expect
# 2001x1125) + house_chrome_check.py gate log; (2) crop pair via
# pick_dense_region.py + the fresh_leg_chain.sh PIL recipe ->
# crop_dense_render_w8.png / crop_dense_orig_w8.png; (3) FULL + CROP vision legs
# launched from the repo root in THIS ONE bash call, ending with wait.
# Never touches the DB, never modifies pptx, never deletes banked evidence.
set -u
ROOT=/home/codespace/ai_llm_slides
cd "$ROOT" || exit 1
NS=videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
N2=${1:?usage: waveW8_slide.sh N2}
N=$((10#$N2))
N3=$(printf %03d "$N")
D=$RJ/slide$N2
PPTX=$NS/recreated_pptx/slide_${N3}_recreated.pptx
ORIG=$NS/unique_slides/slide_${N3}.jpg
export TMPDIR=$ROOT/scratch/tmp
mkdir -p "$TMPDIR" "$D" "$D/w8"
LOG=$RJ/waveW8_slide_${N2}.log
exec >> "$LOG" 2>&1
echo "=== W8 slide $N2 start $(date -u +%FT%TZ) pid=$$"

# (1) render_w8.png via unique-profile soffice + pdftoppm
if [ -f "$D/render_w8.png" ] && [ "$D/render_w8.png" -nt "$PPTX" ]; then
  echo "$N2 render_w8.png fresh: $(python3 -c "from PIL import Image;print(Image.open('$D/render_w8.png').size)")"
else
  echo "$(date -u +%FT%TZ) slide_$N3 $(md5sum "$PPTX")" >> "$RJ/waveW8_md5.txt"
  echo "$N2 rendering w8 $(date -u +%FT%TZ)"
  rm -f "$D/w8/slide_${N3}_recreated.pdf" "$D/render_w8.png"
  soffice --headless "-env:UserInstallation=file://$TMPDIR/lo_w8_$N2" \
    --convert-to pdf "$PPTX" --outdir "$D/w8" > "$D/w8/render_w8_soffice.log" 2>&1
  pdftoppm -png -r 150 -singlefile "$D/w8/slide_${N3}_recreated.pdf" "$D/render_w8" >> "$D/w8/render_w8_soffice.log" 2>&1
  echo "$N2 render_w8.png = $(python3 -c "from PIL import Image;print(Image.open('$D/render_w8.png').size)" 2>/dev/null) $(date -u +%FT%TZ)"
fi
python3 "$NS/shared_patterns/house_chrome_check.py" "$D/render_w8.png" "$N" > "$D/chrome_check_w8.txt" 2>&1
echo "$N2 chrome_check_w8 rc=$? $(tail -1 "$D/chrome_check_w8.txt") $(date -u +%FT%TZ)"

# (2) crop pair per fresh_leg_chain.sh
if [ -f "$D/crop_dense_render_w8.png" ] && [ -f "$D/crop_dense_orig_w8.png" ] && \
   [ "$D/crop_dense_render_w8.png" -nt "$D/render_w8.png" ]; then
  echo "$N2 w8 crop pair fresh"
else
  read -r X0 Y0 X1 Y1 < <(python3 "$RJ/pick_dense_region.py" "$N3")
  echo "$N2 w8 crop region $X0 $Y0 $X1 $Y1"
  python3 - "$D/render_w8.png" "$ORIG" "$D" "$X0" "$Y0" "$X1" "$Y1" <<'PY'
import sys
import numpy as np
from PIL import Image
rp, op, out, x0, y0, x1, y1 = sys.argv[1], sys.argv[2], sys.argv[3], *map(int, sys.argv[4:8])
r = Image.open(rp).convert("RGB"); o = Image.open(op).convert("RGB")
sc = r.size[1] / 540.0
rc = r.crop((int(x0*sc), int(y0*sc), int(np.ceil(x1*sc)), int(np.ceil(y1*sc))))
oc = o.crop((x0, y0, x1, y1)).resize(rc.size, Image.LANCZOS)
rc.save(f"{out}/crop_dense_render_w8.png"); oc.save(f"{out}/crop_dense_orig_w8.png")
PY
  echo "$N2 w8 crops render=$(python3 -c "from PIL import Image;print(Image.open('$D/crop_dense_render_w8.png').size)") orig=$(python3 -c "from PIL import Image;print(Image.open('$D/crop_dense_orig_w8.png').size)") $(date -u +%FT%TZ)"
fi

# (3) FULL + CROP legs, one bash call, ending with wait
OCC_MAX=700 ATTEMPTS=10 setsid nohup bash "$RJ/vision_leg.sh" \
  "$D/judge_full_w8.txt" 600 "$D/render_w8.png" "$ORIG" \
  "Slide $N2 full rejudge W8" "2001x1125 app render vs 960x540 orig" \
  "$RJ/payload_A.txt" > "$D/judge_full_w8.wrapper.out" 2>&1 < /dev/null &
OCC_MAX=700 ATTEMPTS=10 setsid nohup bash "$RJ/vision_leg.sh" \
  "$D/crop_dense_judge_w8.txt" 600 "$D/crop_dense_render_w8.png" "$D/crop_dense_orig_w8.png" \
  "Slide $N2 crop rejudge W8" "dense crop pair" \
  "$RJ/payload_B_025.txt" > "$D/crop_dense_judge_w8.wrapper.out" 2>&1 < /dev/null &
wait
echo "=== W8 slide $N2 legs wait returned $(date -u +%FT%TZ)"
