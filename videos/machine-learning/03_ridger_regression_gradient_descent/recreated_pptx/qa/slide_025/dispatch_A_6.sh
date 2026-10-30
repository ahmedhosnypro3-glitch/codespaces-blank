#!/bin/bash
# Slide 025 Template A full-slide judge, attempt 6 (worker-s4-3730479).
# render_6 = rebuild after breakLine label fix. Payload: judge_prompt_4.txt (frozen Template A).
export TMPDIR=/home/ahmed/Projects/ai_llm_slides/scratch/tmp
cd /home/ahmed/Projects/ai_llm_slides || exit 1
Q=videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide_025
P="$(cat $Q/judge_prompt_4.txt)"
timeout 1700 bash scripts/16_vision_gate.sh python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  $Q/render_6.png \
  videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_025.jpg \
  --view "Slide 025 recreation attempt 6 — fidelity check vs original lecture frame" \
  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  --thinking high --max-tokens 65536 \
  --timeout 1200 --rounds 1 --tries 1 \
  --transcript $Q/judge_attempt_6.txt \
  -p "$P"
echo "EXIT=$?"
