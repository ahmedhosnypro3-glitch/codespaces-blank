#!/usr/bin/env bash
set -e
R="/home/ahmed/Projects/ai_llm_slides"
Q="videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide003"
N=$(pgrep -c -f analyze_image.py 2>/dev/null | head -1); [ -z "$N" ] && N=0
if [ "$N" -ge 8 ]; then echo "GATE CONGESTED ($N) -- not dispatching"; exit 3; fi
cd "$R" && bash scripts/16_vision_gate.sh timeout 1700 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  "$Q/crop_35_bottomright_render.png" \
  "$Q/crop_35_bottomright_orig.png" \
  --view "Slide 003 zoomed crop bottomright — render vs original at matched scale (attempt 35)" \
  --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: the bottom-right box: Y = XW heading, Where: X is a matrix, Y is labels vector" \
  --thinking high --max-tokens 65536 \
  --timeout 1200 --rounds 1 --tries 1 \
  --transcript "$Q/crop_35_bottomright_judge.txt" \
  -p "$(cat $Q/judge_prompt_19_crop.txt)"
