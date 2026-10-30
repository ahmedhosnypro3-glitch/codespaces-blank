#!/usr/bin/env bash
# Rejudge one already-certified slide of deck 03 (Ridge Regression & Gradient Descent).
#   usage: rejudge_slide.sh NNN
# Renders the certified pptx at 150dpi, checks house chrome, then runs BOTH judge legs:
#   leg A = full-slide Template A comparison vs unique_slides/slide_NNN.jpg
#   leg B = zoomed crop-pair Template B over the densest content region
# Writes evidence under recreated_pptx/qa/rejudge_20261027/slideNNN/ and a result file.
# Read-only with respect to the deck: never touches pptx/, build/, unique_slides/ or the DB.
set -u
SLIDE="${1:?usage: rejudge_slide.sh NNN}"
ROOT=/home/codespace/ai_llm_slides
cd "$ROOT" || exit 1
NS=videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
OUT=$RJ/slide$SLIDE
export TMPDIR=$ROOT/scratch/tmp
mkdir -p "$TMPDIR" "$OUT"

PPTX=$NS/recreated_pptx/slide_${SLIDE}_recreated.pptx
if [ ! -f "$PPTX" ]; then echo "MISSING_PPTX $PPTX"; exit 2; fi

TITLE=$(sqlite3 "$NS/slides_progress.db" "SELECT title FROM slides WHERE slide_id=${SLIDE#0};" 2>/dev/null)
[ -n "$TITLE" ] || TITLE="slide $SLIDE"

gate_wait() {
  for _ in $(seq 1 120); do
    n=$(pgrep -c -f analyze_image.py 2>/dev/null || true); n=${n:-0}
    [ "$n" -lt 8 ] && return 0
    sleep 15
  done
  return 0
}

# ---- 1) render 150dpi (unique LO profile so parallel workers never collide) ----
rm -f "$OUT/slide_${SLIDE}_recreated.pdf" "$OUT/render.png"
soffice --headless "-env:UserInstallation=file://$TMPDIR/lo_rejudge_$SLIDE" \
  --convert-to pdf "$PPTX" --outdir "$OUT" > "$OUT/render.log" 2>&1
PDF="$OUT/slide_${SLIDE}_recreated.pdf"
if [ ! -f "$PDF" ]; then echo "RENDER_FAIL"; tail -5 "$OUT/render.log"; exit 3; fi
pdftoppm -png -r 150 -singlefile "$PDF" "$OUT/render" >> "$OUT/render.log" 2>&1
if [ ! -f "$OUT/render.png" ]; then echo "PPM_FAIL"; exit 3; fi
python3 - "$OUT/render.png" <<'PY'
import sys
from PIL import Image
im = Image.open(sys.argv[1])
print("render size", im.size)
PY

# ---- 2) house chrome gate (FAIL = stop, do not spend vision) ----
python3 "$NS/shared_patterns/house_chrome_check.py" "$OUT/render.png" "${SLIDE#0}" > "$OUT/chrome_check.txt" 2>&1
CHROME_RC=$?
cat "$OUT/chrome_check.txt"
if [ "$CHROME_RC" -ne 0 ]; then echo "CHROME_FAIL rc=$CHROME_RC"; exit 4; fi

# ---- 3) densest region -> matched-scale crop pair ----
read -r X0 Y0 X1 Y1 < <(python3 "$RJ/pick_dense_region.py" "$SLIDE")
echo "dense region: $X0 $Y0 $X1 $Y1"
python3 - "$OUT/render.png" "$NS/unique_slides/slide_$SLIDE.jpg" "$OUT" "$X0" "$Y0" "$X1" "$Y1" <<'PY'
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
print("crop render", rc.size, "orig", oc.size, "eff", round(rc.size[0] / (x1 - x0), 3), round(oc.size[0] / (x1 - x0), 3))
PY

# ---- 4) leg A: full-slide Template A ----
gate_wait
timeout 1700 bash scripts/16_vision_gate.sh python3 .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  "$OUT/render.png" "$NS/unique_slides/slide_$SLIDE.jpg" \
  --view "Slide $SLIDE recreation — fidelity check vs original lecture frame" \
  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  --thinking high --max-tokens 65536 --timeout 1200 --rounds 1 --tries 1 \
  --transcript "$OUT/judge_full.txt" \
  -p "$(cat "$RJ/payload_A.txt")" > "$OUT/judge_full.log" 2>&1
FULL_RC=$?
A_OK=0
grep -q "FINAL VERDICT" "$OUT/judge_full.txt" 2>/dev/null && A_OK=1
if [ "$A_OK" -eq 0 ]; then
  echo "leg A no verdict (rc=$FULL_RC) — ONE W4 retry under wider wall"
  sleep 30
  timeout 2100 bash scripts/16_vision_gate.sh python3 .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    "$OUT/render.png" "$NS/unique_slides/slide_$SLIDE.jpg" \
    --view "Slide $SLIDE recreation — fidelity check vs original lecture frame" \
    --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
    --thinking high --max-tokens 65536 --timeout 1800 --rounds 1 --tries 1 \
    --transcript "$OUT/judge_full_retry.txt" \
    -p "$(cat "$RJ/payload_A.txt")" > "$OUT/judge_full_retry.log" 2>&1
  grep -q "FINAL VERDICT" "$OUT/judge_full_retry.txt" 2>/dev/null && A_OK=1
fi

# ---- 5) leg B: zoomed crop-pair Template B ----
PAYLOAD_B=$(sed "s/slide NNN/slide $SLIDE/g" "$RJ/payload_B.tmpl")
gate_wait
timeout 1700 bash scripts/16_vision_gate.sh python3 .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  "$OUT/crop_dense_render.png" "$OUT/crop_dense_orig.png" \
  --view "Slide $SLIDE zoomed crop dense — render vs original at matched scale (rejudge 1)" \
  --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: densest content region of slide $SLIDE (frame px $X0,$Y0-$X1,$Y1) — $TITLE" \
  --thinking high --max-tokens 65536 --timeout 1200 --rounds 1 --tries 1 \
  --transcript "$OUT/crop_dense_judge.txt" \
  -p "$PAYLOAD_B" > "$OUT/crop_dense_judge.log" 2>&1
CROP_RC=$?
B_OK=0
grep -q "FINAL VERDICT" "$OUT/crop_dense_judge.txt" 2>/dev/null && B_OK=1
if [ "$B_OK" -eq 0 ]; then
  echo "leg B no verdict (rc=$CROP_RC) — ONE W4 retry under wider wall"
  sleep 30
  timeout 2100 bash scripts/16_vision_gate.sh python3 .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    "$OUT/crop_dense_render.png" "$OUT/crop_dense_orig.png" \
    --view "Slide $SLIDE zoomed crop dense — render vs original at matched scale (rejudge 1)" \
    --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: densest content region of slide $SLIDE (frame px $X0,$Y0-$X1,$Y1) — $TITLE" \
    --thinking high --max-tokens 65536 --timeout 1800 --rounds 1 --tries 1 \
    --transcript "$OUT/crop_dense_judge_retry.txt" \
    -p "$PAYLOAD_B" > "$OUT/crop_dense_judge_retry.log" 2>&1
  grep -q "FINAL VERDICT" "$OUT/crop_dense_judge_retry.txt" 2>/dev/null && B_OK=1
fi

verdict() {
  if [ "$1" -eq 0 ]; then
    grep -ho "FINAL VERDICT: *\(PASS\|FAIL\)" "$2" | tail -1 | sed 's/.*: *//'
  else
    echo "NORESULT"
  fi
}
FV=$(verdict "$A_OK" "$OUT/judge_full.txt"); [ "$A_OK" -eq 0 ] && FV=$(verdict "$A_OK" "$OUT/judge_full_retry.txt")
BV=$(verdict "$B_OK" "$OUT/crop_dense_judge.txt"); [ "$B_OK" -eq 0 ] && BV=$(verdict "$B_OK" "$OUT/crop_dense_judge_retry.txt")
[ -z "$FV" ] && FV=NORESULT
[ -z "$BV" ] && BV=NORESULT

cat > "$OUT/result.txt" <<EOF
SLIDE=$SLIDE
TITLE=$TITLE
RENDER=$OUT/render.png
REGION=$X0,$Y0-$X1,$Y1
FULL=$FV
CROP=$BV
FULL_TRANSCRIPT=$([ "$A_OK" -eq 1 ] && echo "$OUT/judge_full.txt" || echo "$OUT/judge_full_retry.txt")
CROP_TRANSCRIPT=$([ "$B_OK" -eq 1 ] && echo "$OUT/crop_dense_judge.txt" || echo "$OUT/crop_dense_judge_retry.txt")
EOF
cat "$OUT/result.txt"
echo "REJUDGE_DONE slide=$SLIDE full=$FV crop=$BV"
