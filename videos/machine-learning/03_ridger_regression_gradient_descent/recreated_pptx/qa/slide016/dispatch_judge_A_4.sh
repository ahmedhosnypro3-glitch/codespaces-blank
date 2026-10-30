#!/bin/bash
# worker-016-fix-2: Template A full-slide judge dispatch for slide 016 attempt 4.
# Payload sourced byte-for-byte from shared_patterns/judge_protocol_03.md
# (NNN->016, K->4, word-boundary substitution only; BLOC1ER count verified 0).
set -u
cd /workspaces/codespaces-blank/ai_llm_slides || exit 3
Q=videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide016
exec scripts/16_vision_gate.sh timeout 1700 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  "$Q/render_4.png" \
  "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_016.jpg" \
  --view "Slide 016 recreation attempt 4 — fidelity check vs original lecture frame" \
  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  --thinking high --max-tokens 65536 \
  --timeout 600 --rounds 1 --tries 1 \
  --transcript "$Q/judge_attempt_4.txt" \
  -p "$(cat "$Q/judge_prompt_4A.txt")"
