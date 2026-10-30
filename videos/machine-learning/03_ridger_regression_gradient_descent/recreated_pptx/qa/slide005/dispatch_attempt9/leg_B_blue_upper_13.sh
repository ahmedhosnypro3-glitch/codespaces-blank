#!/usr/bin/env bash
# Leg B — zoomed crop-pair judge, slide 005 attempt 9, region 'blue_upper'.
# Payload sourced byte-for-byte from shared_patterns/judge_protocol_03.md Template B.
set -e
Q="/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide005"
R="/home/ahmed/Projects/ai_llm_slides"
N=$(pgrep -c -f analyze_image.py || echo 0)
if [ "$N" -ge 8 ]; then echo "GATE CONGESTED ($N) -- not dispatching"; exit 3; fi
cd "$R" && bash scripts/16_vision_gate.sh timeout 1700 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide005/crop_13_blue_upper_render.png \
  videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide005/crop_13_blue_upper_orig.png \
  --view "Slide 005 zoomed crop blue_upper — render vs original at matched scale (attempt 9)" \
  --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: $(cat $Q/crop_13_blue_upper_desc.txt)" \
  --thinking high --max-tokens 65536 \
  --timeout 1200 --rounds 1 --tries 1 \
  --transcript videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide005/crop_13_blue_upper_judge.txt \
  -p "$(cat $Q/crop_prompt_9_blue_upper.txt)"
