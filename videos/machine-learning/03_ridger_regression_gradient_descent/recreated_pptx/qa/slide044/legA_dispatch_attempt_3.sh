#!/usr/bin/env bash
# Procedure A full-slide comparison for slide 044, attempt 3 (post-fix render_2.png).
# Reproduces the orchestrator's LEG A invocation exactly; payload bytes unchanged
# (sourced byte-for-byte from judgepayload_legs_A.txt, verified corruption-free).
# Lane wall: --timeout 1200 inside an outer `timeout 1700` wrapper (orchestrator
# directive 2026-10-24). Do NOT extend beyond 1200/1700; no retry loops.
set -u
cd /home/ahmed/Projects/ai_llm_slides || exit 2
V="videos/machine-learning/03_ridger_regression_gradient_descent"
bash scripts/16_vision_gate.sh timeout 1700 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  "$V/recreated_pptx/qa/slide044/render_2.png" \
  "$V/unique_slides/slide_044.jpg" \
  --view "Slide 44 recreation — fidelity check vs original lecture frame" \
  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  --thinking high --max-tokens 65536 --timeout 1200 --rounds 1 --tries 1 \
  --transcript "$V/recreated_pptx/qa/slide044/judge_attempt_3.txt" \
  -p "$(cat "$V/recreated_pptx/qa/slide044/judgepayload_legs_A.txt")"
