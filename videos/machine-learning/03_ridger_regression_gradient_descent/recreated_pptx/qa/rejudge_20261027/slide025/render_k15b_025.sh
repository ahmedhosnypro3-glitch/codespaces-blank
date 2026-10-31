#!/usr/bin/env bash
# render_k15b_025.sh — build slide_025_recreated_k15b.pptx from k15b assets,
# render to render_k15b.png (150dpi, unique LO profile), chrome-check, and
# regenerate the dense crop pair. Vision legs are launched separately.
set -u
ROOT=/home/codespace/ai_llm_slides
cd "$ROOT" || exit 1
NS=videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
OUT=$RJ/slide025
export TMPDIR=$ROOT/scratch/tmp
mkdir -p "$TMPDIR" "$OUT"
N=025

echo "== node build (k15b) =="
K15B_OUT="$OUT/slide_${N}_recreated_k15b.pptx" node "$NS/recreated_pptx/build/slide_025_k15b.js" || exit 2

echo "== render 150dpi (unique LO profile) =="
rm -f "$OUT/slide_${N}_recreated_k15b.pdf" "$OUT/render_k15b.png"
soffice --headless "-env:UserInstallation=file://$TMPDIR/lo_rejudge_${N}_k15b" \
  --convert-to pdf "$OUT/slide_${N}_recreated_k15b.pptx" --outdir "$OUT" > "$OUT/render_k15b.log" 2>&1
PDF="$OUT/slide_${N}_recreated_k15b.pdf"
[ -f "$PDF" ] || { echo RENDER_FAIL; tail -5 "$OUT/render_k15b.log"; exit 3; }
pdftoppm -png -r 150 -singlefile "$PDF" "$OUT/render_k15b" >> "$OUT/render_k15b.log" 2>&1
[ -f "$OUT/render_k15b.png" ] || { echo PPM_FAIL; exit 3; }
python3 -c "from PIL import Image; print('render_k15b size', Image.open('$OUT/render_k15b.png').size)"

echo "== chrome check =="
python3 "$NS/shared_patterns/house_chrome_check.py" "$OUT/render_k15b.png" 25 > "$OUT/chrome_check_k15b.txt" 2>&1
RC=$?
cat "$OUT/chrome_check_k15b.txt"
[ "$RC" -ne 0 ] && { echo CHROME_FAIL; exit 4; }

echo "== dense crop pair (region 592 160 896 368) =="
read -r X0 Y0 X1 Y1 < <(python3 "$RJ/pick_dense_region.py" "$N")
echo "dense region: $X0 $Y0 $X1 $Y1"
python3 - "$OUT/render_k15b.png" "$NS/unique_slides/slide_$N.jpg" "$OUT" "$X0" "$Y0" "$X1" "$Y1" <<'PY'
import sys
import numpy as np
from PIL import Image
rp, op, out, x0, y0, x1, y1 = sys.argv[1], sys.argv[2], sys.argv[3], *map(int, sys.argv[4:8])
r = Image.open(rp).convert("RGB")
o = Image.open(op).convert("RGB")
sc = r.size[1] / 540.0
rc = r.crop((int(x0 * sc), int(y0 * sc), int(np.ceil(x1 * sc)), int(np.ceil(y1 * sc))))
oc = o.crop((x0, y0, x1, y1)).resize(rc.size, Image.LANCZOS)
rc.save(f"{out}/crop_dense_render_k15b.png")
oc.save(f"{out}/crop_dense_orig.png")
print("crop render", rc.size, "orig", oc.size)
PY
echo "RENDER_K15B_DONE"
