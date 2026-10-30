#!/bin/bash
# Slide 025 Template A full-slide judge, attempt K=4 (detached).
# Payload: qa/slide_025/judge_prompt_4.txt == frozen Template A verbatim (verified).
export TMPDIR=/workspaces/codespaces-blank/ai_llm_slides/scratch/tmp
cd /workspaces/codespaces-blank/ai_llm_slides || exit 1
P="$(cat videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide_025/judge_prompt_4.txt)"
exec timeout 1700 bash scripts/16_vision_gate.sh python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide_025/render_4.png \
  videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_025.jpg \
  --view "Slide 025 recreation attempt 4 — fidelity check vs original lecture frame" \
  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  --thinking high --max-tokens 65536 \
  --timeout 1200 --rounds 1 --tries 1 \
  --transcript videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide_025/judge_attempt_4.txt \
  -p "$P"
