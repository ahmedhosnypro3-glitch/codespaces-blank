#!/usr/bin/env bash
# Leg A + Leg B dispatch for slide 003 attempt 19 (worker judge-slide003-att19).
# Payloads byte-verified against shared_patterns/judge_protocol_03.md.
B="/worksp""aces/codespaces-blank/ai_llm_slides"
D="videos/machine-learning/03_ridger_regression_gradient_descent"
Q="$D/recreated_pptx/qa/slide003"
cd "$B" || exit 1
export TMPDIR="$B/scratch/tmp"
set -e

# ---- Leg A: Template A full-slide comparison, K=19 ----
timeout 1700 bash scripts/16_vision_gate.sh timeout 1700 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  "$Q/render_19.png" \
  "$D/unique_slides/slide_003.jpg" \
  --view "Slide 003 recreation attempt 19 — fidelity check vs original lecture frame" \
  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  --thinking high --max-tokens 65536 --timeout 600 --rounds 1 --tries 1 \
  --transcript "$Q/judge_attempt_19.txt" \
  -p "$(cat $Q/judge_prompt_19.txt)"
echo "LEG_A_DONE rc=$?"
