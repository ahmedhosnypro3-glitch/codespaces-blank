#!/usr/bin/env bash
# promote_k17b_025.sh <winning_assets_dir> — backup-promoter promotion of a
# qualifying k17 asset set for slide 025:
#   bank deliverable -> swap build/assets PNGs (old backed up) -> node build
#   -> unique-profile LO render to render_k17b.png -> chrome check -> dense
#   crop pair -> launch both judge legs OCC_MAX=700 (judge_full_k17b.txt 1200s,
#   crop_dense_judge_k17b.txt 600s). DB/deck updates are a separate step after
#   clean FULL=PASS + CROP=PASS.
set -u
ROOT=/home/codespace/ai_llm_slides
cd "$ROOT" || exit 1
NS=videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
D=$RJ/slide025
WIN_DIR=$1
[ -d "$D/$WIN_DIR" ] || { echo "no such dir $WIN_DIR"; exit 1; }
export TMPDIR=$ROOT/scratch/tmp
mkdir -p "$TMPDIR" "$D" "$RJ/legs_20261031.pids"
N=025

echo "== DB pre-check (must not be passed/PASS) =="
sqlite3 "$NS/slides_progress.db" ".timeout 20000" "SELECT slide_id,gen_status,visual_check FROM slides WHERE slide_id=25;"
ST=$(sqlite3 "$NS/slides_progress.db" ".timeout 20000" "SELECT gen_status||'/'||coalesce(visual_check,'') FROM slides WHERE slide_id=25;")
if [ "$ST" = "passed/PASS" ]; then echo "ALREADY_PASSED — abort"; exit 9; fi

echo "== bank current deliverable =="
cp -p "$NS/recreated_pptx/slide_${N}_recreated.pptx" "$D/slide_${N}_recreated.preK17b.bak.pptx"
md5sum "$NS/recreated_pptx/slide_${N}_recreated.pptx" "$D/slide_${N}_recreated.preK17b.bak.pptx"

echo "== swap winning PNGs into build/assets (old backed up) =="
mkdir -p "$D/assets_preK17b"
for n in tl tr bl br; do
  cp -p "$NS/recreated_pptx/build/assets/plot_025_$n.png" "$D/assets_preK17b/plot_025_$n.png"
  cp "$D/$WIN_DIR/plot_025_$n.png" "$NS/recreated_pptx/build/assets/plot_025_$n.png"
done
md5sum "$D/$WIN_DIR"/plot_025_*.png "$NS/recreated_pptx/build/assets/plot_025_*.png"

echo "== node build =="
cd "$NS/recreated_pptx/build" || exit 2
node slide_025.js || exit 2
cd "$ROOT"
md5sum "$NS/recreated_pptx/slide_${N}_recreated.pptx"

echo "== render 150dpi (unique LO profile) to render_k17b.png =="
rm -f "$D/slide_${N}_recreated.pdf" "$D/render_k17b.png"
soffice --headless "-env:UserInstallation=file://$TMPDIR/lo_rejudge_${N}_k17b" \
  --convert-to pdf "$NS/recreated_pptx/slide_${N}_recreated.pptx" --outdir "$D" > "$D/render_k17b.log" 2>&1
[ -f "$D/slide_${N}_recreated.pdf" ] || { echo RENDER_FAIL; tail -5 "$D/render_k17b.log"; exit 3; }
pdftoppm -png -r 150 -singlefile "$D/slide_${N}_recreated.pdf" "$D/render_k17b" >> "$D/render_k17b.log" 2>&1
[ -f "$D/render_k17b.png" ] || { echo PPM_FAIL; exit 3; }
python3 -c "from PIL import Image; print('render_k17b size', Image.open('$D/render_k17b.png').size)"

echo "== chrome check =="
python3 "$NS/shared_patterns/house_chrome_check.py" "$D/render_k17b.png" 25 > "$D/chrome_check_k17b.txt" 2>&1
RC=$?
cat "$D/chrome_check_k17b.txt"
[ "$RC" -ne 0 ] && { echo CHROME_FAIL; exit 4; }

echo "== dense crop pair from render_k17b.png =="
read -r X0 Y0 X1 Y1 < <(python3 "$RJ/pick_dense_region.py" "$N")
echo "dense region: $X0 $Y0 $X1 $Y1"
python3 - "$D/render_k17b.png" "$NS/unique_slides/slide_$N.jpg" "$D" "$X0" "$Y0" "$X1" "$Y1" <<'PY'
import sys
import numpy as np
from PIL import Image
rp, op, out, x0, y0, x1, y1 = sys.argv[1], sys.argv[2], sys.argv[3], *map(int, sys.argv[4:8])
r = Image.open(rp).convert("RGB")
o = Image.open(op).convert("RGB")
sc = r.size[1] / 540.0
rc = r.crop((int(x0 * sc), int(y0 * sc), int(np.ceil(x1 * sc)), int(np.ceil(y1 * sc))))
oc = o.crop((x0, y0, x1, y1)).resize(rc.size, Image.LANCZOS)
rc.save(f"{out}/crop_dense_render_k17b.png")
oc.save(f"{out}/crop_dense_orig_k17b.png")
print("crop render", rc.size, "orig", oc.size)
PY

echo "== launch legs OCC_MAX=700 =="
NN=25
OCC_MAX=700 setsid nohup bash "$RJ/vision_leg.sh" "$D/judge_full_k17b.txt" 1200 \
  "$D/render_k17b.png" "$NS/unique_slides/slide_$N.jpg" \
  "Slide $NN recreation — fidelity check vs original lecture frame (k17b)" \
  "IMG1=150dpi PNG render of 13.33x7.5in PPTX; IMG2=original 960x540 lecture frame" \
  "$RJ/payload_A.txt" > "$D/judge_full_k17b.wrapper.out" 2>&1 < /dev/null &
echo $! > "$RJ/legs_20261031.pids/${N}_full_k17b.pid"
echo "launched full_k17b pid $!"

OCC_MAX=700 setsid nohup bash "$RJ/vision_leg.sh" "$D/crop_dense_judge_k17b.txt" 600 \
  "$D/crop_dense_render_k17b.png" "$D/crop_dense_orig_k17b.png" \
  "Slide $NN zoomed crop — fidelity check vs original (k17b)" \
  "IMG1=zoomed crop of 150dpi render; IMG2=matched-scale crop of original frame" \
  "$RJ/payload_B_$N.txt" > "$D/crop_dense_judge_k17b.wrapper.out" 2>&1 < /dev/null &
echo $! > "$RJ/legs_20261031.pids/${N}_crop_k17b.pid"
echo "launched crop_k17b pid $!"
echo "PROMOTE_K17B_DONE winner=$WIN_DIR"
