#!/usr/bin/env bash
# Template A (full-slide comparison) judge for slide 034, attempt 6 (render_4).
# Payload banked byte-for-byte from shared_patterns/judge_protocol_03.md Template A.
set -u
cd /workspaces/codespaces-blank/ai_llm_slides
export TMPDIR=/workspaces/codespaces-blank/ai_llm_slides/scratch/tmp
B=videos/machine-learning/03_ridger_regression_gradient_descent
Q=$B/recreated_pptx/qa/slide034
scripts/16_vision_gate.sh timeout 1700 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  $Q/render_6.png \
  $B/unique_slides/slide_034.jpg \
  --view "Slide 034 recreation — fidelity check vs original lecture frame" \
  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  --thinking high --max-tokens 65536 \
  --timeout 600 --rounds 1 --tries 1 \
  --transcript $Q/judge_attempt_6.txt \
  -p "$(cat $Q/judge_prompt_6.txt)"
