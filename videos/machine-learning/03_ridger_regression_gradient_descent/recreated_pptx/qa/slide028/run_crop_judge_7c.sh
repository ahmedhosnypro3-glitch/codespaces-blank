#!/usr/bin/env bash
set -u
ROOT=/workspaces/codespaces-blank/ai_llm_slides
export TMPDIR=/workspaces/codespaces-blank/ai_llm_slides/scratch/tmp
QA=$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide028
TS="$QA/crop_7c_right_curve_judge.txt"
PAYLOAD=$(sed 's/NNN/28/g' "$QA/payload_template_B.txt")
DESC="right chart panel x480..865 y180..470 — the U-shaped loss curve, its gradient-descent step markers crossing the valley, and the valley floor"
echo "=== crop leg on render_7 (single call, timeout 1700) start $(date +%T) ===" | tee -a "$QA/crop_7c_retry.log"
cd "$ROOT" && timeout 1700 bash scripts/16_vision_gate.sh python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  "$QA/crop_7_right_curve_render.png" \
  "$QA/crop_7_right_curve_orig.png" \
  --view "Slide 028 zoomed crop right_curve — render vs original at matched scale (attempt 7)" \
  --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: ${DESC}" \
  --thinking high --max-tokens 65536 \
  --timeout 600 --rounds 1 --tries 1 \
  --transcript "$TS" \
  -p "$PAYLOAD" 2>&1 | tail -20 | tee -a "$QA/crop_7c_retry.log"
if grep -q "FINAL VERDICT" "$TS" 2>/dev/null; then
  echo "==> VERDICT BANKED" | tee -a "$QA/crop_7c_retry.log"; tail -3 "$TS" | tee -a "$QA/crop_7c_retry.log"
else
  echo "==> NO VERDICT" | tee -a "$QA/crop_7c_retry.log"
fi
