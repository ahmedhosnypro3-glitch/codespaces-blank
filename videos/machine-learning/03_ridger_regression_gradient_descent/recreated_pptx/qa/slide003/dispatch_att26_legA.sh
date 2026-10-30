#!/usr/bin/env bash
set -e
R="/home/ahmed/Projects/ai_llm_slides"
Q="videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide003"
N=$(pgrep -c -f analyze_image.py || echo 0)
if [ "$N" -ge 8 ]; then echo "GATE CONGESTED ($N) -- not dispatching"; exit 3; fi
cd "$R" && bash scripts/16_vision_gate.sh timeout 1700 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  "$Q/render_26.png" \
  videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_003.jpg \
  --view "Slide 003 recreation attempt 26 — fidelity check vs original lecture frame" \
  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  --thinking high --max-tokens 65536 \
  --timeout 1200 --rounds 1 --tries 1 \
  --transcript "$Q/judge_attempt_26.txt" \
  -p "$(cat "$Q/judge_prompt_19.txt")"
