#!/usr/bin/env bash
# LEG 1 — Template A full-slide comparison judge, slide 021 attempt 10 (render_10.png)
# Payload byte-for-byte from shared_patterns/judge_protocol_03.md Template A
# (banked: qa/slide021/judge_prompt_10.txt, 4116 chars).
set -u
ROOT="/workspaces/codespaces-blank/ai_llm_slides"
QADIR="$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide021"
PAYLOAD="$(cat "$QADIR/judge_prompt_10.txt")"
cd "$ROOT" && scripts/16_vision_gate.sh timeout 1700 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide021/render_10.png \
  videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_021.jpg \
  --view "Slide 021 recreation attempt 10 — fidelity check vs original lecture frame" \
  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  --thinking high --max-tokens 65536 \
  --timeout 600 --rounds 1 --tries 1 \
  --transcript videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide021/judge_attempt_10.txt \
  -p "$PAYLOAD"
