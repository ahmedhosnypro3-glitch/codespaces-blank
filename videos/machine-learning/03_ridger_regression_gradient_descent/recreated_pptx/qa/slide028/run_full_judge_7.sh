#!/usr/bin/env bash
set -u
ROOT=/workspaces/codespaces-blank/ai_llm_slides
export TMPDIR=/workspaces/codespaces-blank/ai_llm_slides/scratch/tmp
export VIDEO=machine-learning/03_ridger_regression_gradient_descent
QA=$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide028
TS="$QA/judge_attempt_5.txt"
LOG="$QA/judge_retry_7.log"
PAYLOAD=$(cat "$QA/payload_template_A.txt")
echo "=== Template A judge: slide 028 render_7 (single call) start $(date +%T) ===" | tee -a "$LOG"
cd "$ROOT" && scripts/16_vision_gate.sh timeout 1700 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  "$QA/render_7.png" \
  "$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_028.jpg" \
  --view "Slide 028 recreation — fidelity check vs original lecture frame" \
  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  --thinking high --max-tokens 65536 \
  --timeout 600 --rounds 1 --tries 1 \
  --transcript "$TS" \
  -p "$PAYLOAD" 2>&1 | tail -12 | tee -a "$LOG"
if grep -q "FINAL VERDICT" "$TS" 2>/dev/null; then
  echo "==> VERDICT BANKED" | tee -a "$LOG"; tail -2 "$TS" | tee -a "$LOG"
else
  echo "==> NO VERDICT (hang/abort)" | tee -a "$LOG"
fi
