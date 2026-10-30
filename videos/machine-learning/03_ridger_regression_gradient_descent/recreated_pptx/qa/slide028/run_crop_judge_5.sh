#!/usr/bin/env bash
# Procedure B crop-pair judge runner for slide 028 — Template B payload VERBATIM.
# ONE vision call per invocation (no retry loop): a hang with no banked body
# charges no attempt under protocol law, so the caller re-invokes deliberately.
set -u
ROOT=/workspaces/codespaces-blank/ai_llm_slides
export TMPDIR=/workspaces/codespaces-blank/ai_llm_slides/scratch/tmp
export VIDEO=machine-learning/03_ridger_regression_gradient_descent
QA=$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide028
NAME="$1"; DESC="$2"
TS="$QA/crop_5_${NAME}_judge.txt"
PAYLOAD=$(sed 's/NNN/28/g' "$QA/payload_template_B.txt")
LOG="$QA/crop_5_${NAME}_retry.log"

echo "=== crop judge: $NAME (single call) start $(date +%T) ===" | tee -a "$LOG"
echo "region: $DESC" | tee -a "$LOG"

cd "$ROOT" && scripts/16_vision_gate.sh timeout 1700 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  "$QA/crop_5_${NAME}_render.png" \
  "$QA/crop_5_${NAME}_orig.png" \
  --view "Slide 028 zoomed crop ${NAME} — render vs original at matched scale (attempt 5)" \
  --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: ${DESC}" \
  --thinking high --max-tokens 65536 \
  --timeout 600 --rounds 1 --tries 1 \
  --transcript "$TS" \
  -p "$PAYLOAD" 2>&1 | tail -20 | tee -a "$LOG"
if grep -q "FINAL VERDICT" "$TS" 2>/dev/null; then
  echo "==> VERDICT BANKED for $NAME" | tee -a "$LOG"
  tail -3 "$TS" | tee -a "$LOG"
  exit 0
fi
echo "==> NO VERDICT for $NAME (hang/abort — protocol-legal to re-invoke once)" | tee -a "$LOG"
exit 1
