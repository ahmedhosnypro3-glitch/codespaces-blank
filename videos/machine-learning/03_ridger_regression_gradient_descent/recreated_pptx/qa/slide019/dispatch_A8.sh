#!/usr/bin/env bash
set -u
export TMPDIR=/workspaces/codespaces-blank/ai_llm_slides/scratch/tmp
cd /workspaces/codespaces-blank/ai_llm_slides
VID=videos/machine-learning/03_ridger_regression_gradient_descent
Q=$VID/recreated_pptx/qa/slide019
echo "GATE-LOAD-START: $(pgrep -c -f analyze_image.py)"
scripts/16_vision_gate.sh timeout 1700 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  $Q/render_8.png $VID/unique_slides/slide_019.jpg \
  --view "Slide 019 recreation attempt 8 - fidelity check vs original lecture frame" \
  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  --thinking high --max-tokens 65536 --timeout 600 --rounds 1 --tries 1 \
  --transcript $Q/judge_attempt_8.txt \
  -p "$(cat $Q/judgeA8_payload_20261024.txt)"
echo "EXIT=$?"
