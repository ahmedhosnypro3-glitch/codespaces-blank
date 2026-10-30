#!/usr/bin/env bash
# Dispatch one Procedure B crop-pair judge (Template B, verbatim payload).
# Usage: dispatch_crop_judge.sh <NAME> <TRANSCRIPT>
# NOTE: re-cut crops from the CURRENT render before use.
set -e
cd /workspaces/codespaces-blank/ai_llm_slides
export TMPDIR=/workspaces/codespaces-blank/ai_llm_slides/scratch/tmp
Q=videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide046
NAME="$1"
TX="$2"
P=$(cat "$Q/templateB_payload.txt")

case "$NAME" in
  plot)      DESC="red-bordered Cartesian scatter plot (frame x312..825, y173..482): 13 blue squares, 9 magenta diamonds, 7 red triangles, the red decision line at data x=3, interior tick labels" ;;
  zmatrix)   DESC="top-centre Z matrix (frame x597..657, y60..111): Z1 Z1 Z1 header row, then two digit rows (0,0,7)/(0,6,2) enclosed by three tall parenthesis pairs" ;;
  augtable)  DESC="lower-left augmented-vectors box (frame x69..246, y140..255): dashed separator, x1..x6 subscript header, three data rows, C1/C2 class row, bottom rule at y255, full box border" ;;
  yellowbox) DESC="top-right yellow final-weight box (frame x738..828, y59..142): underlined W, =, and the three-row column vector (14,-4,0) between tall parenthesis strokes" ;;
  stopbox)   DESC="mid/lower-left callouts (frame x84..245, y277..415): solid-red 'Iteration 4' box with white bold text, and pink 'Stop Iterations' box with 'No change in W' plus red bold 'Stop Iterations'" ;;
  caption)   DESC="class-legend caption (frame x251..508, y110..124): 'C1 positive C2 negative Zero is unaccepted' with C1 blue, C2 red, Zero green" ;;
  *) echo "unknown NAME $NAME"; exit 2 ;;
esac

bash scripts/16_vision_gate.sh timeout 1700 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  "$Q/crop_2_${NAME}_render.png" \
  "$Q/crop_2_${NAME}_orig.png" \
  --view "Slide 046 zoomed crop ${NAME} — render vs original at matched scale (attempt 2)" \
  --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: ${DESC}" \
  --thinking high --max-tokens 65536 \
  --timeout 600 --rounds 1 --tries 1 \
  --transcript "$Q/${TX}" \
  -p "$P"
