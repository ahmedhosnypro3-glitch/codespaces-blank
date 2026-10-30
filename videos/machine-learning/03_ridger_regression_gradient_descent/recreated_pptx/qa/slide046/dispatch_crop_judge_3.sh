#!/usr/bin/env bash
# Dispatch ONE Procedure B crop-pair judge for slide 046 (Template B, verbatim payload).
# Crops are re-cut from render_3.png (crop_3_<name>_*), matched effective scale.
# Usage: dispatch_crop_judge_3.sh <NAME> <TRANSCRIPT>
set -e
cd "/worksp""aces/codespaces-blank/ai_llm_slides"
export TMPDIR=/workspaces/codespaces-blank/ai_llm_slides/scratch/tmp
Q=videos/machine-learning/03_ridger_reggression_gradient_descent/recreated_pptx/qa/slide046
NAME="$1"
TX="$2"
P=$(cat "$Q/templateB_payload.txt")

case "$NAME" in
  plot)      DESC="red-bordered Cartesian scatter plot (frame x312..825, y173..482): three blue squares at (1,2)(1,1)(2,1), three magenta diamonds at (6,6)(6,5)(5,4), three red triangles at (7,6)(3,2)(0,0), a vertical red decision line at data x~3.478, and interior tick labels on both axes (0..8 x, 0..7 y)" ;;
  zmatrix)   DESC="top-centre Z matrix (frame x597..657, y60..111): Z1 Z1 Z1 subscript header row, then two digit rows 0 0 7 and 0 6 2, enclosed by three tall parenthesis pairs spanning the digit rows" ;;
  augtable)  DESC="lower-left augmented-vectors box (frame x69..246, y140..255): dashed top separator, x1..x6 subscript header, three data rows (1 2 1 5 6 4 / 1 1 2 4 5 6 / 1 1 1 4 5 6), C1 C1 C1 C2 C2 C2 class row, a navy left border, and a solid rule at y255" ;;
  yellowbox) DESC="top-right pale-yellow final-weight box (frame x738..828, y59..142): underlined W, an equals sign, and the three-row column vector 14 / -4 / 0 between two tall parenthesis strokes" ;;
  stopbox)   DESC="mid/lower-left callouts (frame x84..245, y277..415): a SOLID RED 'Iteration 4' box with white bold text, and a pink 'Stop Iterations' box containing 'No change in W' (W underlined) over red bold 'Stop Iterations'" ;;
  caption)   DESC="class-legend caption (frame x251..508, y110..124): 'C1 positive C2 negative Zero is unaccepted' with C1 blue, C2 red, and Zero green" ;;
  *) echo "unknown NAME $NAME"; exit 2 ;;
esac

bash scripts/16_vision_gate.sh timeout 1700 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  "$Q/crop_3_${NAME}_render.png" \
  "$Q/crop_3_${NAME}_orig.png" \
  --view "Slide 046 zoomed crop ${NAME} — render vs original at matched scale (attempt 3)" \
  --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: ${DESC}" \
  --thinking high --max-tokens 65536 \
  --timeout 600 --rounds 1 --tries 1 \
  --transcript "$Q/${TX}" \
  -p "$P"
