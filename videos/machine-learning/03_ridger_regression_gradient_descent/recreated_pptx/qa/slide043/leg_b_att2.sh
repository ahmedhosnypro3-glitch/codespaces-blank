#!/bin/bash
set -e
NAME="$1"
cd /home/ahmed/Projects/ai_llm_slides
scripts/16_vision_gate.sh timeout 1700 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide043/crop_2_${NAME}_render.png \
  videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide043/crop_2_${NAME}_orig.png \
  --view "Slide 043 zoomed crop ${NAME} — render vs original at matched scale (attempt 2)" \
  --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: $(cat videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide043/crop_2_${NAME}_desc.txt)" \
  --thinking high --max-tokens 65536 \
  --timeout 1200 --rounds 1 --tries 1 \
  --transcript videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide043/crop_2_${NAME}_judge.txt \
  -p "$(cat videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide043/judgepayload_att2_B_${NAME}.txt)"
