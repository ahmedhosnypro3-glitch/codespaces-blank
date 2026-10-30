#!/usr/bin/env bash
# Leg B — zoomed crop-pair judge, slide 005 attempt 14, region 'lower_eqs'.
# Payload sourced byte-for-byte from shared_patterns/judge_protocol_03.md Template B.
set -e
Q="/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide005"
R="/home/ahmed/Projects/ai_llm_slides"
N=$(pgrep -c -f analyze_image.py || echo 0)
if [ "$N" -ge 8 ]; then echo "GATE CONGESTED ($N) -- not dispatching"; exit 3; fi
cd "$R" && bash scripts/16_vision_gate.sh timeout 1700 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide005/crop_14_lower_eqs_render.png \
  videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide005/crop_14_lower_eqs_orig.png \
  --view "Slide 005 zoomed crop lower_eqs — render vs original at matched scale (attempt 14)" \
  --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: $(cat $Q/crop_14_lower_eqs_desc.txt)" \
  --thinking high --max-tokens 65536 \
  --timeout 1200 --rounds 1 --tries 1 \
  --transcript videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide005/crop_14_lower_eqs_judge.txt \
  -p "$(cat $Q/crop_prompt_9_lower_eqs.txt)"
