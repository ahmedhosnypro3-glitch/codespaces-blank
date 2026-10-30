#!/usr/bin/env bash
# Probe — Template A probe block, slide 005 attempt 15 (render_15.png).
set -e
cd /home/ahmed/Projects/ai_llm_slides && bash scripts/16_vision_gate.sh timeout 150 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py analysis \
  videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide005/render_15.png \
  --view "Slide 005 recreation attempt 15 — probe" \
  --capture "150dpi PNG render of a 13.33x7.5in PPTX" \
  --timeout 120 --rounds 1 --tries 1 \
  --transcript videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide005/probe_15.txt
