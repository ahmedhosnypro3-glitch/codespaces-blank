#!/bin/bash
# Slide 025 Procedure B crop-pair judges, attempt K=4 (detached sequential loop).
# Payloads: qa/slide_025/crop_prompt_4_<name>.txt == frozen Template B with
# NNN->025 only (byte-verified in verify_4.txt). Pairs cut from render_4.png at
# matched effective scale (see cut_crops_4.py output).
export TMPDIR=/workspaces/codespaces-blank/ai_llm_slides/scratch/tmp
cd /workspaces/codespaces-blank/ai_llm_slides || exit 1
QA=videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide_025
for NAME in title lbl_upper lbl_lower tl tr bl br; do
  case "$NAME" in
    title)     DESC="the red title text 'Types of Loss function shapes'";;
    lbl_upper) DESC="the top-gutter blue caption boxes beside the TL and TR figure boxes";;
    lbl_lower) DESC="the bottom-gutter blue caption boxes beside the BL and BR figure boxes";;
    tl)        DESC="the top-left white figure: thin red border, concave dome jet surface, two red horizontal reference lines";;
    tr)        DESC="the top-right white figure: thin red border, convex bowl jet surface, axis ticks with x10^4 scale, two red reference lines";;
    bl)        DESC="the bottom-left white figure: thin red border, non-convex multi-extremum surface, red reference line, two red annotation arrows, four black Global/Local annotations";;
    br)        DESC="the bottom-right white figure: thin red border, valley jet surface, black gradient-descent path with arrowheads";;
  esac
  P="$(cat $QA/crop_prompt_4_$NAME.txt)"
  echo "=== crop $NAME dispatch $(date -u +%H:%M:%S) ==="
  timeout 1700 bash scripts/16_vision_gate.sh python3 \
    .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    $QA/crop_4_${NAME}_render.png \
    $QA/crop_4_${NAME}_orig.png \
    --view "Slide 025 zoomed crop $NAME — render vs original at matched scale (attempt 4)" \
    --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: $DESC" \
    --thinking high --max-tokens 65536 \
    --timeout 1200 --rounds 1 --tries 1 \
    --transcript $QA/crop_4_${NAME}_judge.txt \
    -p "$P"
  echo "=== crop $NAME done rc=$? $(date -u +%H:%M:%S) ==="
done
echo "ALL CROPS DONE $(date -u +%H:%M:%S)"
