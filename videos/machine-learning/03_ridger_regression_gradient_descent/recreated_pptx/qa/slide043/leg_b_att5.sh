#!/bin/bash
set -e
NAME="$1"
cd /home/codespace/ai_llm_slides
V=videos/machine-learning/03_ridger_regression_gradient_descent
timeout 1700 bash scripts/16_vision_gate.sh python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  $V/recreated_pptx/qa/slide043/crop_5_${NAME}_render.png \
  $V/recreated_pptx/qa/slide043/crop_5_${NAME}_orig.png \
  --view "Slide 043 zoomed crop ${NAME} — render vs original at matched scale (attempt 5)" \
  --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: $(cat $V/recreated_pptx/qa/slide043/crop_5_${NAME}_desc.txt)" \
  --thinking high --max-tokens 65536 \
  --timeout 600 --rounds 1 --tries 1 \
  --transcript $V/recreated_pptx/qa/slide043/crop_5_${NAME}_judge.txt \
  -p "$(cat $V/recreated_pptx/qa/slide043/judgepayload_att5_B_${NAME}.txt)"
