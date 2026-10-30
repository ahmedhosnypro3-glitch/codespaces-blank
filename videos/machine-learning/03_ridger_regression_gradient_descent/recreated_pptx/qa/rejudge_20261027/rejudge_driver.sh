#!/usr/bin/env bash
# Detached rejudge driver for deck 03 (Ridge Regression & Gradient Descent).
#   usage: rejudge_driver.sh <SCOPE> <NNN> [NNN...]
# Per slide: render 150dpi, chrome gate, matched-scale dense crop pair,
# leg A (full-slide Template A) unless a verdict is already banked,
# leg B (zoomed crop-pair Template B), then writes slideNNN/result.txt.
# Reuses banked judge_full.txt verbatim when it already carries a FINAL VERDICT
# (render bytes are deterministic from the pptx).
# Survives session exit: intended to be launched with setsid/nohup.
set -u
SCOPE="${1:?usage: rejudge_driver.sh SCOPE NNN [NNN...]}"
shift
ROOT=/home/codespace/ai_llm_slides
cd "$ROOT" || exit 1
NS=videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
export TMPDIR=$ROOT/scratch/tmp
mkdir -p "$TMPDIR"
LOG=$RJ/driver_${SCOPE}.log
echo "[driver $SCOPE] start $(date -u +%F_%T) slides: $*" >> "$LOG"

gate_wait() {
  for _ in $(seq 1 40); do
    n=$(pgrep -c -f analyze_image.py 2>/dev/null || true); n=${n:-0}
    [ "$n" -lt 8 ] && return 0
    sleep 15
  done
  return 0
}

for SLIDE in "$@"; do
  OUT=$RJ/slide$SLIDE
  if [ -f "$OUT/result.txt" ]; then echo "[driver $SCOPE] $SLIDE already done" >> "$LOG"; continue; fi
  echo "[driver $SCOPE] $SLIDE begin $(date -u +%T)" >> "$LOG"
  mkdir -p "$OUT"
  PPTX=$NS/recreated_pptx/slide_${SLIDE}_recreated.pptx
  if [ ! -f "$PPTX" ]; then echo "[driver $SCOPE] $SLIDE MISSING_PPTX" >> "$LOG"; continue; fi
  TITLE=$(sqlite3 "$NS/slides_progress.db" "SELECT title FROM slides WHERE slide_id=${SLIDE#0};" 2>/dev/null)
  [ -n "$TITLE" ] || TITLE="slide $SLIDE"

  rm -f "$OUT/slide_${SLIDE}_recreated.pdf" "$OUT/render.png"
  soffice --headless "-env:UserInstallation=file://$TMPDIR/lo_rej_${SCOPE}_${SLIDE}" \
    --convert-to pdf "$PPTX" --outdir "$OUT" > "$OUT/render.log" 2>&1
  PDF="$OUT/slide_${SLIDE}_recreated.pdf"
  if [ ! -f "$PDF" ]; then echo "[driver $SCOPE] $SLIDE RENDER_FAIL" >> "$LOG"; continue; fi
  pdftoppm -png -r 150 -singlefile "$PDF" "$OUT/render" >> "$OUT/render.log" 2>&1
  [ -f "$OUT/render.png" ] || { echo "[driver $SCOPE] $SLIDE PPM_FAIL" >> "$LOG"; continue; }

  python3 "$NS/shared_patterns/house_chrome_check.py" "$OUT/render.png" "${SLIDE#0}" > "$OUT/chrome_check.txt" 2>&1
  if [ $? -ne 0 ]; then echo "[driver $SCOPE] $SLIDE CHROME_FAIL" >> "$LOG"; continue; fi

  read -r X0 Y0 X1 Y1 < <(python3 "$RJ/pick_dense_region.py" "$SLIDE")
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
PY

  # ---- leg A: full-slide Template A (reuse banked verdict when present) ----
  A_OK=0
  if grep -q "FINAL VERDICT" "$OUT/judge_full.txt" 2>/dev/null; then
    A_OK=1; echo "[driver $SCOPE] $SLIDE reusing banked full verdict" >> "$LOG"
  else
    gate_wait
    echo "[driver $SCOPE] $SLIDE leg A dispatch $(date -u +%T)" >> "$LOG"
    timeout 1700 bash scripts/16_vision_gate.sh python3 .agents/skills/image-analysis/scripts/analyze_image.py comparison \
      "$OUT/render.png" "$NS/unique_slides/slide_$SLIDE.jpg" \
      --view "Slide $SLIDE recreation — fidelity check vs original lecture frame" \
      --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
      --thinking high --max-tokens 65536 --timeout 1200 --rounds 1 --tries 1 \
      --transcript "$OUT/judge_full.txt" \
      -p "$(cat "$RJ/payload_A.txt")" > "$OUT/judge_full.log" 2>&1
    grep -q "FINAL VERDICT" "$OUT/judge_full.txt" 2>/dev/null && A_OK=1
    echo "[driver $SCOPE] $SLIDE leg A done A_OK=$A_OK $(date -u +%T)" >> "$LOG"
    if [ "$A_OK" -eq 0 ]; then
      echo "[driver $SCOPE] $SLIDE leg A no verdict — ONE W4 retry $(date -u +%T)" >> "$LOG"
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
  fi

  # ---- leg B: zoomed crop-pair Template B ----
  B_OK=0
  PAYLOAD_B=$(sed "s/slide NNN/slide $SLIDE/g" "$RJ/payload_B.tmpl")
  if grep -q "FINAL VERDICT" "$OUT/crop_dense_judge.txt" 2>/dev/null; then
    B_OK=1
  else
    gate_wait
    echo "[driver $SCOPE] $SLIDE leg B dispatch $(date -u +%T)" >> "$LOG"
    timeout 1700 bash scripts/16_vision_gate.sh python3 .agents/skills/image-analysis/scripts/analyze_image.py comparison \
      "$OUT/crop_dense_render.png" "$OUT/crop_dense_orig.png" \
      --view "Slide $SLIDE zoomed crop dense — render vs original at matched scale (rejudge 1)" \
      --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: densest content region of slide $SLIDE (frame px $X0,$Y0-$X1,$Y1) — $TITLE" \
      --thinking high --max-tokens 65536 --timeout 1200 --rounds 1 --tries 1 \
      --transcript "$OUT/crop_dense_judge.txt" \
      -p "$PAYLOAD_B" > "$OUT/crop_dense_judge.log" 2>&1
    grep -q "FINAL VERDICT" "$OUT/crop_dense_judge.txt" 2>/dev/null && B_OK=1
    echo "[driver $SCOPE] $SLIDE leg B done B_OK=$B_OK $(date -u +%T)" >> "$LOG"
    if [ "$B_OK" -eq 0 ]; then
      echo "[driver $SCOPE] $SLIDE leg B no verdict — ONE W4 retry $(date -u +%T)" >> "$LOG"
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
  fi

  verdict() {
    if [ "$1" -eq 0 ]; then echo NORESULT; else grep -hoE "FINAL VERDICT: *\*{0,2} *(PASS|FAIL)" "$2" | tail -1 | grep -oE "(PASS|FAIL)"; fi
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
  sqlite3 "$NS/slides_progress.db" ".timeout 15000" "UPDATE slides SET visual_attempts=visual_attempts+1 WHERE slide_id=${SLIDE#0};" 2>/dev/null
  echo "[driver $SCOPE] $SLIDE DONE full=$FV crop=$BV $(date -u +%T)" >> "$LOG"
done
echo "[driver $SCOPE] all done $(date -u +%T)" >> "$LOG"
