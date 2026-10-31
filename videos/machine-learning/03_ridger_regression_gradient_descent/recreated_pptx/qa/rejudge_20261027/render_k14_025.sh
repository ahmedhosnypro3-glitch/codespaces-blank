#!/usr/bin/env bash
# render_k14_025.sh — rebuild slide_025_recreated.pptx from k14 assets, re-render
# to the rejudge dir, chrome-check, regenerate the dense crop pair. Then the two
# vision legs are relaunched separately via launch_leg.sh 025 full|crop.
set -u
ROOT=/home/codespace/ai_llm_slides
cd "$ROOT" || exit 1
NS=videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
OUT=$RJ/slide025
export TMPDIR=$ROOT/scratch/tmp
mkdir -p "$TMPDIR" "$OUT"
N=025

echo "== node build =="
node "$NS/recreated_pptx/build/slide_025.js" || exit 2

echo "== render 150dpi (unique LO profile) =="
rm -f "$OUT/slide_${N}_recreated.pdf" "$OUT/render.png"
soffice --headless "-env:UserInstallation=file://$TMPDIR/lo_rejudge_${N}_k14" \
  --convert-to pdf "$NS/recreated_pptx/slide_${N}_recreated.pptx" --outdir "$OUT" > "$OUT/render_k14.log" 2>&1
PDF="$OUT/slide_${N}_recreated.pdf"
[ -f "$PDF" ] || { echo RENDER_FAIL; tail -5 "$OUT/render_k14.log"; exit 3; }
pdftoppm -png -r 150 -singlefile "$PDF" "$OUT/render" >> "$OUT/render_k14.log" 2>&1
[ -f "$OUT/render.png" ] || { echo PPM_FAIL; exit 3; }
python3 -c "from PIL import Image; print('render size', Image.open('$OUT/render.png').size)"

echo "== chrome check =="
python3 "$NS/shared_patterns/house_chrome_check.py" "$OUT/render.png" 25 > "$OUT/chrome_check.txt" 2>&1
RC=$?
cat "$OUT/chrome_check.txt"
[ "$RC" -ne 0 ] && { echo CHROME_FAIL; exit 4; }

echo "== dense crop pair =="
read -r X0 Y0 X1 Y1 < <(python3 "$RJ/pick_dense_region.py" "$N")
echo "dense region: $X0 $Y0 $X1 $Y1"
python3 - "$OUT/render.png" "$NS/unique_slides/slide_$N.jpg" "$OUT" "$X0" "$Y0" "$X1" "$Y1" <<'PY'
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
echo "RENDER_K14_DONE"
