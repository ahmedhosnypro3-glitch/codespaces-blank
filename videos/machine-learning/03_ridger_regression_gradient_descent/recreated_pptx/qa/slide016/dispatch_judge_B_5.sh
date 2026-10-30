#!/bin/bash
# worker-016-finish-20261024: Procedure B crop-pair judge dispatch for slide 016, attempt 5.
# payload = shared_patterns/judge_protocol_03.md Template B (NNN->016, K->5 only).
set -u
NAME="${1:-missing_band}"
cd /workspaces/codespaces-blank/ai_llm_slides || exit 3
Q=videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide016
case "$NAME" in
  missing_band) DESC="body text lines L7-L10 inside the white content box (both blue L2/L1 key terms + red emphasis runs)" ;;
  bullet2)      DESC="bullet 2's three lines: 'Since there is a contradiction...' + 'the regularization term...' + 'customized weigh factor' + the yellow highlight and the red underline" ;;
  last_bullet)  DESC="the last bullet's small-text cluster: red (N)/(d), 'Large vector Length', and the dark underline under Length" ;;
  *) echo "unknown region $NAME" >&2; exit 2 ;;
esac
exec scripts/16_vision_gate.sh timeout 1700 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  "$Q/crop_5_${NAME}_render.png" \
  "$Q/crop_5_${NAME}_orig.png" \
  --view "Slide 016 zoomed crop ${NAME} — render vs original at matched scale (attempt 5)" \
  --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: ${DESC}" \
  --thinking high --max-tokens 65536 \
  --timeout 600 --rounds 1 --tries 1 \
  --transcript "$Q/crop_5_${NAME}_judge.txt" \
  -p "$(cat "$Q/judge_prompt_5B.txt")"
