#!/bin/bash
# Leg 2 — Procedure B zoomed crop-pair judge, slide 033, attempt 12 (crop_12_*).
# Usage: dispatch_crop_k12.sh <region>   (region = plot | table | center | title)
# Payload: judge_payload_B_k9.txt — byte-for-byte from
#   shared_patterns/judge_protocol_03.md Template B (protocol line 117),
#   one mandated `slide NNN` -> `slide 33` substitution; md5
#   0b5a221efbbe91481de2882e3bafbb4b, len 1923 (unchanged).
# Lane wall (orchestrator directive 2026-10-24): analyzer --timeout 1200 inside
#   `timeout 1700`, --rounds 1 --tries 1, --thinking high --max-tokens 65536.
# No retry loops around this gate.
set -u
REGION="${1:-plot}"
cd /workspaces/codespaces-blank/ai_llm_slides || exit 1
Q=videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide033

case "$REGION" in
  plot)   DESC="the non-convex curve with its gridlines, the red initial-point marker, the orange arrowhead, the green square at the reached minimum, the pale pink Reach Local Minima callout, and both tick-label rows" ;;
  table)  DESC="the data table with its fill bands, all eight text rows and every header/value cell" ;;
  center) DESC="the f(x) = (x^2 cos(x)-x)/10 equation callout with its two annotation lines" ;;
  title)  DESC="the slide title and both subtitle lines" ;;
  *) echo "unknown region: $REGION"; exit 2 ;;
esac

bash scripts/16_vision_gate.sh timeout 1700 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  $Q/crop_12_${REGION}_render.png $Q/crop_12_${REGION}_orig.png \
  --view "Slide 33 zoomed crop $REGION — render vs original at matched scale (attempt 12)" \
  --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: $DESC" \
  --thinking high --max-tokens 65536 \
  --timeout 1200 --rounds 1 --tries 1 \
  --transcript $Q/crop_12_${REGION}_judge.txt \
  -p "$(cat $Q/judge_payload_B_k9.txt)"
echo "CROP_${REGION}_GATE_EXIT=$?"
