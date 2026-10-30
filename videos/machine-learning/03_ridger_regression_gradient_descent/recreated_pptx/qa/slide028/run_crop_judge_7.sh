#!/usr/bin/env bash
set -u
ROOT=/workspaces/codespaces-blank/ai_llm_slides
export TMPDIR=/workspaces/codespaces-blank/ai_llm_slides/scratch/tmp
export VIDEO=machine-learning/03_ridger_regression_gradient_descent
QA=$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide028
NAME=right_curve
DESC="right chart panel x480..865 y180..470 — the U-shaped loss curve, its gradient-descent step markers crossing the valley, and the valley floor"
TS="$QA/crop_7_${NAME}_judge.txt"
PAYLOAD=$(sed 's/NNN/28/g' "$QA/payload_template_B.txt")
LOG="$QA/crop_7_${NAME}_retry.log"
echo "=== crop judge: $NAME (single call) start $(date +%T) ===" | tee -a "$LOG"
cd "$ROOT" && scripts/16_vision_gate.sh timeout 1700 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  "$QA/crop_7_${NAME}_render.png" \
  "$QA/crop_7_${NAME}_orig.png" \
  --view "Slide 028 zoomed crop ${NAME} — render vs original at matched scale (attempt 7)" \
  --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: ${DESC}" \
  --thinking high --max-tokens 65536 \
  --timeout 600 --rounds 1 --tries 1 \
  --transcript "$TS" \
  -p "$PAYLOAD" 2>&1 | tail -20 | tee -a "$LOG"
if grep -q "FINAL VERDICT" "$TS" 2>/dev/null; then
  echo "==> VERDICT BANKED for $NAME" | tee -a "$LOG"; tail -3 "$TS" | tee -a "$LOG"
else
  echo "==> NO VERDICT for $NAME (hang/abort)" | tee -a "$LOG"
fi
