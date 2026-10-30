#!/usr/bin/env bash
# Leg A — full-slide comparison judge, slide 005 attempt 9 (render_9.png).
# Payload sourced byte-for-byte from shared_patterns/judge_protocol_03.md Template A.
set -e
Q="/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide005"
R="/home/ahmed/Projects/ai_llm_slides"
N=$(pgrep -c -f analyze_image.py || echo 0)
if [ "$N" -ge 8 ]; then echo "GATE CONGESTED ($N) -- not dispatching"; exit 3; fi
cd "$R" && bash scripts/16_vision_gate.sh timeout 1700 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide005/render_12.png \
  videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_005.jpg \
  --view "Slide 005 recreation — fidelity check vs original lecture frame" \
  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  --thinking high --max-tokens 65536 \
  --timeout 1200 --rounds 1 --tries 1 \
  --transcript videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide005/judge_attempt_12.txt \
  -p "$(cat "$Q/judge_prompt_9.txt")"
