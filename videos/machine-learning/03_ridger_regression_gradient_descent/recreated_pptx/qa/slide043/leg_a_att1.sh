#!/bin/bash
set -e
cd /home/ahmed/Projects/ai_llm_slides
scripts/16_vision_gate.sh timeout 1700 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide043/render_1.png \
  videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_043.jpg \
  --view "Slide 043 recreation — fidelity check vs original lecture frame" \
  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  --thinking high --max-tokens 65536 \
  --timeout 1200 --rounds 1 --tries 1 \
  --transcript videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide043/judge_attempt_1.txt \
  -p "$(cat videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide043/judgepayload_att1_A.txt)"
