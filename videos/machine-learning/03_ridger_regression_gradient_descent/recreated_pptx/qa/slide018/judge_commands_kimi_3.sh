#!/usr/bin/env bash
# Slide 018 Leg A, attempt 3 (kimi-slide018, 2026-10-25) — after the attempt-2
# FAIL fixes (y-row ink black, mark rect removed, norm skeleton redrawn).
# Template A payload byte-identical to the banked judge_prompt_1.txt.
set -u
export TMPDIR=/home/ahmed/Projects/ai_llm_slides/scratch/tmp
cd /home/ahmed/Projects/ai_llm_slides
QA=videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide018

COUNT=$(pgrep -c -f analyze_image.py || true)
if [ "${COUNT:-99}" -ge 8 ]; then
  echo "=== GATE BUSY (analyze_image.py count=${COUNT}) — not dispatching ==="
  exit 75
fi

scripts/16_vision_gate.sh timeout 1700 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  $QA/render_3.png \
  videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_018.jpg \
  --view "Slide 018 recreation — fidelity check vs original lecture frame (attempt 3)" \
  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  --thinking high --max-tokens 65536 \
  --timeout 1200 --rounds 1 --tries 1 \
  --transcript $QA/judge_attempt_3.txt \
  -p "$(cat $QA/judge_prompt_1.txt)"
