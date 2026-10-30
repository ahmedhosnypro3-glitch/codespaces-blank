#!/usr/bin/env bash
# Slide 044 certification dispatch (deck 03): leg A full-slide Template A +
# crop legs (densest region + eqstack/lmbox(topband/lefttables) bands) via the
# fleet vision gate only. Payloads: rejudge payload_A.txt verbatim,
# payload_B.tmpl with "slide NNN" -> "slide 044". Run from $ROOT.
set -u
ROOT=/home/codespace/ai_llm_slides
cd "$ROOT"
NS=videos/machine-learning/03_ridger_regression_gradient_descent
QA=$NS/recreated_pptx/qa/slide044
RJ=$NS/recreated_pptx/qa/rejudge_20261027
export TMPDIR=$ROOT/scratch/tmp
RENDER=$QA/render_2.png
ORIG=$NS/unique_slides/slide_044.jpg

gate_wait() {
  for _ in $(seq 1 240); do
    n=$(pgrep -c -f analyze_image.py 2>/dev/null || true); n=${n:-0}
    if [ "$n" -lt 8 ]; then echo "[gate] free (n=$n) $(date -u +%T)"; return 0; fi
    sleep 15
  done
  echo "[gate] wait exhausted, proceeding"
}

# ---- matched-scale crop pairs from render_2 + original ----
read -r X0 Y0 X1 Y1 < <(python3 "$RJ/pick_dense_region.py" 044)
echo "dense region: $X0 $Y0 $X1 $Y1"
python3 - "$RENDER" "$ORIG" "$QA" "$X0" "$Y0" "$X1" "$Y1" <<'PY'
import sys
import numpy as np
from PIL import Image
rp, op, out, x0, y0, x1, y1 = sys.argv[1], sys.argv[2], sys.argv[3], *map(int, sys.argv[4:8])
r = Image.open(rp).convert("RGB"); o = Image.open(op).convert("RGB")
sc = r.size[1] / 540.0
rc = r.crop((int(x0*sc), int(y0*sc), int(np.ceil(x1*sc)), int(np.ceil(y1*sc))))
oc = o.crop((x0, y0, x1, y1)).resize(rc.size, Image.LANCZOS)
rc.save(f"{out}/crop_2_dense_render.png"); oc.save(f"{out}/crop_2_dense_orig.png")
print("dense", rc.size, oc.size)
PY
python3 - "$RENDER" "$ORIG" "$QA" <<'PY'
import sys
import numpy as np
from PIL import Image
rp, op, out = sys.argv[1:4]
r = Image.open(rp).convert("RGB"); o = Image.open(op).convert("RGB")
sc = r.size[1] / 540.0
REGIONS = {
    "eqstack":    (272, 136, 856, 532),
    "lefttables": (66, 52, 252, 312),
    "centretext": (236, 52, 730, 132),
}
for name, (x0, y0, x1, y1) in REGIONS.items():
    rc = r.crop((int(x0*sc), int(y0*sc), int(np.ceil(x1*sc)), int(np.ceil(y1*sc))))
    oc = o.crop((x0, y0, x1, y1)).resize(rc.size, Image.LANCZOS)
    rc.save(f"{out}/crop_2_{name}_render.png"); oc.save(f"{out}/crop_2_{name}_orig.png")
    print(name, rc.size, oc.size)
PY

# ---- leg A: full-slide Template A, --timeout 1200 ----
gate_wait
timeout 1700 bash scripts/16_vision_gate.sh python3 .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  "$RENDER" "$ORIG" \
  --view "Slide 044 recreation — fidelity check vs original lecture frame" \
  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  --thinking high --max-tokens 65536 --timeout 1200 --rounds 1 --tries 1 \
  --transcript "$QA/judge_att1_full.txt" \
  -p "$(cat "$RJ/payload_A.txt")" > "$QA/judge_att1_full.log" 2>&1
echo "leg A rc=$? $(date -u +%T)"

# ---- crop legs: Template B, --timeout 600 ----
PAYLOAD_B=$(sed "s/slide NNN/slide 044/g" "$RJ/payload_B.tmpl")
for name in dense eqstack lefttables centretext; do
  gate_wait
  timeout 1000 bash scripts/16_vision_gate.sh python3 .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    "$QA/crop_2_${name}_render.png" "$QA/crop_2_${name}_orig.png" \
    --view "Slide 044 zoomed crop $name — render vs original at matched scale (attempt 1)" \
    --capture "IMG1=zoomed crop of a 150dpi PPTX render (render_2, scale 2.0833 vs 960x540 frame); IMG2=the SAME slide-space region cropped from unique_slides/slide_044.jpg and upscaled to matched effective scale; region: $name crop of slide 044" \
    --thinking high --max-tokens 65536 --timeout 600 --rounds 1 --tries 1 \
    --transcript "$QA/judge_att1_crop_${name}.txt" \
    -p "$PAYLOAD_B" > "$QA/judge_att1_crop_${name}.log" 2>&1
  echo "crop $name rc=$? $(date -u +%T)"
done

for f in judge_att1_full judge_att1_crop_dense judge_att1_crop_eqstack judge_att1_crop_lefttables judge_att1_crop_centretext; do
  v=$(grep -ho "FINAL VERDICT: *\(PASS\|FAIL\)" "$QA/$f.txt" 2>/dev/null | tail -1)
  echo "$f: ${v:-NOVERDICT}"
done | tee "$QA/judge_att1_summary.txt"
echo DISPATCH_DONE $(date -u +%T)
