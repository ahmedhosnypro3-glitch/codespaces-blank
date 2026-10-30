#!/usr/bin/env bash
# Procedure B crop-pair judges for slide 034 (attempt 2).
# Payloads are banked byte-for-byte from shared_patterns/judge_protocol_03.md (Template B).
# Usage: bash judge_crops_2.sh <table|plot> <transcript-name>
set -u
cd /workspaces/codespaces-blank/ai_llm_slides
export TMPDIR=/workspaces/codespaces-blank/ai_llm_slides/scratch/tmp
B=videos/machine-learning/03_ridger_regression_gradient_descent
NAME="${1:?region name}"
TRANSCRIPT="${2:?transcript filename}"
REGION_DESC=""
case "$NAME" in
  table)
    REGION_DESC="the 8-row x 19-column numeric gradient-descent table (x, f(x), x-delta, f(x-delta), x+delta, f(x+delta), slope, next x) with its coloured row fills and green highlight cells"
    ;;
  plot)
    REGION_DESC="the 2D plot of the non-convex function f(x)=(x^2 cos(x)-x)/10: blue curve, red step markers, orange arrow, pink 'Reach global Minima' annotation, axes and ticks"
    ;;
  *) echo "unknown region $NAME" >&2; exit 2 ;;
esac

# Substitute the region description into --capture only (the -p payload is invariant).
scripts/16_vision_gate.sh timeout 1700 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  "$B/recreated_pptx/qa/slide034/crop_2_${NAME}_render.png" \
  "$B/recreated_pptx/qa/slide034/crop_2_${NAME}_orig.png" \
  --view "Slide 034 zoomed crop ${NAME} — render vs original at matched scale (attempt 2)" \
  --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: ${REGION_DESC}" \
  --thinking high --max-tokens 65536 \
  --timeout 600 --rounds 1 --tries 1 \
  --transcript "$B/recreated_pptx/qa/slide034/${TRANSCRIPT}" \
  -p "$(cat "$B/recreated_pptx/qa/slide034/crop_${NAME}_prompt_2.txt")"
