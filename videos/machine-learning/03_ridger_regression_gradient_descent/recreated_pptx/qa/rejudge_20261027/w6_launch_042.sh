#!/usr/bin/env bash
# w6_launch_042.sh — wave W6 dense-crop rejudge leg for the one gap slide (042).
# Gap definition: newest crop_dense_judge*.txt under slide042/ missing or lacking a
# clean FINAL VERDICT (no 429). Never touches DB/pptx; writes only under $RJ + scratch.
set -u
ROOT=/home/codespace/ai_llm_slides
cd "$ROOT" || exit 1
NS=videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
D=$ROOT/$RJ/slide042
N=042
export TMPDIR=$ROOT/scratch/tmp
mkdir -p "$TMPDIR" "$D"
echo "=== W6 launch slide $N start $(date -u +%FT%TZ) pid=$$"

# render: reuse render.png when newer than the pptx, else fresh unique-profile render
PPTX=$ROOT/$NS/recreated_pptx/slide_${N}_recreated.pptx
if [ -f "$D/render.png" ] && [ ! "$PPTX" -nt "$D/render.png" ]; then
  R=$D/render.png
  echo "--- $N reuse render.png (pptx not newer)"
else
  rm -f "$D/slide_${N}_recreated.pdf"
  soffice --headless "-env:UserInstallation=file://$TMPDIR/lo_w6_${N}" \
    --convert-to pdf "$PPTX" --outdir "$D" > "$D/render_w6.log" 2>&1
  pdftoppm -png -r 150 -singlefile "$D/slide_${N}_recreated.pdf" "$D/render_w6" >> "$D/render_w6.log" 2>&1
  R=$D/render_w6.png
  echo "--- $N fresh render -> render_w6.png"
fi

# w6 crop pair via the fresh_leg_chain.sh recipe (pick_dense_region.py)
read -r X0 Y0 X1 Y1 < <(python3 "$RJ/pick_dense_region.py" "$N")
echo "--- $N crop region $X0 $Y0 $X1 $Y1"
python3 - "$R" "$ROOT/$NS/unique_slides/slide_${N}.jpg" "$D" "$X0" "$Y0" "$X1" "$Y1" <<'PY'
import sys
import numpy as np
from PIL import Image
rp, op, out, x0, y0, x1, y1 = sys.argv[1], sys.argv[2], sys.argv[3], *map(int, sys.argv[4:8])
r = Image.open(rp).convert("RGB"); o = Image.open(op).convert("RGB")
sc = r.size[1] / 540.0
rc = r.crop((int(x0*sc), int(y0*sc), int(np.ceil(x1*sc)), int(np.ceil(y1*sc))))
oc = o.crop((x0, y0, x1, y1)).resize(rc.size, Image.LANCZOS)
rc.save(f"{out}/crop_dense_render_w6.png"); oc.save(f"{out}/crop_dense_orig_w6.png")
print("WXH=%dx%d" % rc.size)
PY
WXH=$(python3 -c "from PIL import Image; print('%dx%d' % Image.open('$D/crop_dense_render_w6.png').size)")
echo "--- $N crop pair w6 built: $WXH"

OCC_MAX=700 ATTEMPTS=10 setsid nohup bash "$RJ/vision_leg.sh" \
  "$D/crop_dense_judge_w6.txt" 600 "$D/crop_dense_render_w6.png" "$D/crop_dense_orig_w6.png" \
  "Slide $N dense-crop rejudge W6" "$WXH crop pair, app render" "$RJ/payload_B_${N}.txt" &
wait
echo "=== W6 launch slide $N end $(date -u +%FT%TZ)"
if [ -f "$D/crop_dense_judge_w6.txt" ] && grep -q 'FINAL VERDICT' "$D/crop_dense_judge_w6.txt" && ! grep -qi '429' "$D/crop_dense_judge_w6.txt"; then
  echo "W6_RESULT slide $N $(grep -oE 'FINAL VERDICT: *\*{0,2} *(PASS|FAIL)' "$D/crop_dense_judge_w6.txt" | tail -1)"
else
  echo "W6_RESULT slide $N NORESULT"
fi
