#!/usr/bin/env bash
# promote_k15b_025.sh — bank the current deliverable, promote the k15b pptx,
# re-render render.png (unique LO profile), chrome-check, refresh the dense
# crop pair, and launch both vision legs with OCC_MAX=700 writing
# judge_full_k15b.txt / crop_dense_judge_k15b.txt.
set -u
ROOT=/home/codespace/ai_llm_slides
cd "$ROOT" || exit 1
NS=videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
D=$RJ/slide025
export TMPDIR=$ROOT/scratch/tmp
mkdir -p "$TMPDIR" "$D" "$RJ/legs_20261031.pids"
N=025

echo "== bank current deliverable =="
cp -p "$NS/recreated_pptx/slide_${N}_recreated.pptx" "$D/slide_${N}_recreated_pre_k15b_bank.pptx"
md5sum "$NS/recreated_pptx/slide_${N}_recreated.pptx" "$D/slide_${N}_recreated_pre_k15b_bank.pptx"

echo "== promote k15b =="
cp "$D/slide_${N}_recreated_k15b.pptx" "$NS/recreated_pptx/slide_${N}_recreated.pptx"
md5sum "$NS/recreated_pptx/slide_${N}_recreated.pptx" "$D/slide_${N}_recreated_k15b.pptx"

echo "== re-render render.png from promoted deliverable =="
rm -f "$D/slide_${N}_recreated.pdf" "$D/render.png"
soffice --headless "-env:UserInstallation=file://$TMPDIR/lo_rejudge_${N}_k15c" \
  --convert-to pdf "$NS/recreated_pptx/slide_${N}_recreated.pptx" --outdir "$D" > "$D/render_promote_k15b.log" 2>&1
[ -f "$D/slide_${N}_recreated.pdf" ] || { echo RENDER_FAIL; tail -5 "$D/render_promote_k15b.log"; exit 3; }
pdftoppm -png -r 150 -singlefile "$D/slide_${N}_recreated.pdf" "$D/render" >> "$D/render_promote_k15b.log" 2>&1
[ -f "$D/render.png" ] || { echo PPM_FAIL; exit 3; }
python3 -c "from PIL import Image; print('render.png size', Image.open('$D/render.png').size)"

echo "== chrome check on promoted render =="
python3 "$NS/shared_patterns/house_chrome_check.py" "$D/render.png" 25 > "$D/chrome_check_promoted_k15b.txt" 2>&1
RC=$?
cat "$D/chrome_check_promoted_k15b.txt"
[ "$RC" -ne 0 ] && { echo CHROME_FAIL; exit 4; }

echo "== refresh dense crop pair from promoted render.png =="
read -r X0 Y0 X1 Y1 < <(python3 "$RJ/pick_dense_region.py" "$N")
echo "dense region: $X0 $Y0 $X1 $Y1"
python3 - "$D/render.png" "$NS/unique_slides/slide_$N.jpg" "$D" "$X0" "$Y0" "$X1" "$Y1" <<'PY'
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
print("crop render", rc.size, "orig", oc.size)
PY

echo "== launch legs OCC_MAX=700 =="
NN=25
OCC_MAX=700 setsid nohup bash "$RJ/vision_leg.sh" "$D/judge_full_k15b.txt" 1200 \
  "$D/render.png" "$NS/unique_slides/slide_$N.jpg" \
  "Slide $NN recreation — fidelity check vs original lecture frame" \
  "IMG1=150dpi PNG render of 13.33x7.5in PPTX; IMG2=original 960x540 lecture frame" \
  "$RJ/payload_A.txt" > "$D/judge_full_k15b.wrapper.out" 2>&1 &
echo $! > "$RJ/legs_20261031.pids/${N}_full_k15b.pid"
echo "launched full_k15b pid $!"

OCC_MAX=700 setsid nohup bash "$RJ/vision_leg.sh" "$D/crop_dense_judge_k15b.txt" 600 \
  "$D/crop_dense_render.png" "$D/crop_dense_orig.png" \
  "Slide $NN zoomed crop — fidelity check vs original" \
  "IMG1=zoomed crop of 150dpi render; IMG2=matched-scale crop of original frame" \
  "$RJ/payload_B_$N.txt" > "$D/crop_dense_judge_k15b.wrapper.out" 2>&1 &
echo $! > "$RJ/legs_20261031.pids/${N}_crop_k15b.pid"
echo "launched crop_k15b pid $!"
echo "PROMOTE_K15B_DONE"
