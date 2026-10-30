#!/bin/bash
set -e
cd /home/codespace/ai_llm_slides
V=videos/machine-learning/03_ridger_regression_gradient_descent
timeout 1700 bash scripts/16_vision_gate.sh python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  $V/recreated_pptx/qa/slide043/render_6.png \
  $V/unique_slides/slide_043.jpg \
  --view "Slide 043 recreation — fidelity check vs original lecture frame (attempt 5)" \
  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX (2001x1125); IMG2=original 960x540 lecture video frame" \
  --thinking high --max-tokens 65536 \
  --timeout 1200 --rounds 1 --tries 1 \
  --transcript $V/recreated_pptx/qa/slide043/judge_attempt_5.txt \
  -p "$(cat $V/recreated_pptx/qa/slide043/judgepayload_att5_A.txt)"
