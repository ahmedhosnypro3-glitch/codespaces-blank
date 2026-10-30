#!/usr/bin/env bash
# Template A full-slide comparison — slide 028, render_5 (attempt 3).
# Payload sourced verbatim from shared_patterns/judge_protocol_03.md Template A.
# ONE vision call per invocation (no retry loop): the gateway is congested, and a
# hang with no banked body charges no attempt under protocol law, so the caller
# re-invokes deliberately rather than spinning here.
set -u
ROOT=/workspaces/codespaces-blank/ai_llm_slides
export TMPDIR=/workspaces/codespaces-blank/ai_llm_slides/scratch/tmp
export VIDEO=machine-learning/03_ridger_regression_gradient_descent
QA=$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide028
TS="$QA/judge_attempt_3.txt"
LOG="$QA/judge_retry_5.log"
PAYLOAD=$(cat "$QA/payload_template_A.txt")

echo "=== Template A judge: slide 028 render_5 (single call) start $(date +%T) ===" | tee -a "$LOG"
cd "$ROOT" && scripts/16_vision_gate.sh timeout 1700 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  "$QA/render_5.png" \
  "$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_028.jpg" \
  --view "Slide 028 recreation — fidelity check vs original lecture frame" \
  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  --thinking high --max-tokens 65536 \
  --timeout 600 --rounds 1 --tries 1 \
  --transcript "$TS" \
  -p "$PAYLOAD" 2>&1 | tail -12 | tee -a "$LOG"
if grep -q "FINAL VERDICT" "$TS" 2>/dev/null; then
  echo "==> VERDICT BANKED" | tee -a "$LOG"; tail -2 "$TS" | tee -a "$LOG"; exit 0
fi
echo "==> NO VERDICT (hang/abort — protocol-legal to re-invoke once)" | tee -a "$LOG"; exit 1
