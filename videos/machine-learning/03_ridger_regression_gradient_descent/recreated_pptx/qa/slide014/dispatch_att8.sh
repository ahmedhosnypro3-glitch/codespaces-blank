#!/usr/bin/env bash
# Slide 014 deck-03 certification attempt 8: full-slide leg + zoomed crop leg,
# both dispatched in parallel in ONE gate window (gate occupancy checked first).
set -u
ROOT=/home/codespace/ai_llm_slides
cd "$ROOT" || exit 1
NS=videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
QA=$NS/recreated_pptx/qa/slide014
RENDER=$QA/render_10.png
ORIG=$NS/unique_slides/slide_014.jpg
export TMPDIR=$ROOT/scratch/tmp
mkdir -p "$TMPDIR"

# gate occupancy: < 8 analyze_image.py processes
gate_wait() {
  for _ in $(seq 1 120); do
    n=$(pgrep -c -f analyze_image.py 2>/dev/null || true); n=${n:-0}
    [ "$n" -lt 8 ] && { echo "gate free (n=$n)"; return 0; }
    sleep 15
  done
  echo "gate still busy after 30min; dispatching anyway"
}
gate_wait

# densest region -> matched-scale crop pair (same method as rejudge_slide.sh)
read -r X0 Y0 X1 Y1 < <(python3 "$RJ/pick_dense_region.py" 014)
echo "dense region: $X0 $Y0 $X1 $Y1"
python3 - "$RENDER" "$ORIG" "$QA" "$X0" "$Y0" "$X1" "$Y1" <<'PY'
import sys
import numpy as np
from PIL import Image
rp, op, out, x0, y0, x1, y1 = sys.argv[1], sys.argv[2], sys.argv[3], *map(int, sys.argv[4:8])
r = Image.open(rp).convert("RGB")
o = Image.open(op).convert("RGB")
sc = r.size[1] / 540.0
rc = r.crop((int(x0 * sc), int(y0 * sc), int(np.ceil(x1 * sc)), int(np.ceil(y1 * sc))))
oc = o.crop((x0, y0, x1, y1)).resize(rc.size, Image.LANCZOS)
rc.save(f"{out}/crop_dense_render_att8.png")
oc.save(f"{out}/crop_dense_orig_att8.png")
print("crop render", rc.size, "orig", oc.size)
PY

PAYLOAD_B=$(sed "s/slide NNN/slide 014/g" "$RJ/payload_B.tmpl")

# ---- leg A: full-slide comparison (Template A payload) ----
timeout 1700 bash scripts/16_vision_gate.sh python3 .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  "$RENDER" "$ORIG" \
  --view "Slide 14 — deck 03 certification, full-slide comparison" \
  --capture "2001x1125 px render @150dpi (scale 2.0833 vs 960x540 original), app lane" \
  --thinking high --max-tokens 65536 --timeout 1200 --rounds 1 --tries 1 \
  --transcript "$QA/judge_att8_full.txt" \
  -p "$(cat "$RJ/payload_A.txt")" > "$QA/judge_att8_full.log" 2>&1 &
A_PID=$!

# ---- leg B: zoomed crop-pair over densest region (Template B payload, inner 600) ----
timeout 1700 bash scripts/16_vision_gate.sh python3 .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  "$QA/crop_dense_render_att8.png" "$QA/crop_dense_orig_att8.png" \
  --view "Slide 014 zoomed crop dense — render vs original at matched scale (attempt 8)" \
  --capture "IMG1=zoomed crop of the 150dpi render (render_10, scale 2.0833 vs 960x540 frame); IMG2=same slide-space region $X0,$Y0-$X1,$Y1 of unique_slides/slide_014.jpg upscaled to matched effective scale; densest content region of slide 014" \
  --thinking high --max-tokens 65536 --timeout 600 --rounds 1 --tries 1 \
  --transcript "$QA/judge_att8_crop.txt" \
  -p "$PAYLOAD_B" > "$QA/judge_att8_crop.log" 2>&1 &
B_PID=$!

wait $A_PID; A_RC=$?
wait $B_PID; B_RC=$?
echo "leg A rc=$A_RC leg B rc=$B_RC"
echo "FULL: $(grep -hoE 'FINAL VERDICT: *\*{0,2} *(PASS|FAIL)' "$QA/judge_att8_full.txt" 2>/dev/null | tail -1)"
echo "CROP: $(grep -hoE 'FINAL VERDICT: *\*{0,2} *(PASS|FAIL)' "$QA/judge_att8_crop.txt" 2>/dev/null | tail -1)"
echo "ATT8_DISPATCH_DONE"
