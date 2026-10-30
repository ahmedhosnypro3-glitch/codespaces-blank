#!/usr/bin/env bash
# Slide 015 — attempt-7 Procedure B crop-pair judge (Template B), one region per call:
#   dispatch_7_crop.sh <eq_stack|pinkbox|peachbox|deriv_stack|solution>
# Crop pairs: crop_6_<slug>_{render,orig}.png, cut by cut_crops_6.py from render_6
# (fresh render of the UNCHANGED slide_015_recreated.pptx) at matched effective scale.
# Payload: recreated_pptx/qa/rejudge_20261027/payload_B.tmpl with the only legal
# substitution slide NNN -> slide 015 (md5 110aa1c75d36a5972ee62043a5ab2da3).
set -u
cd /home/codespace/ai_llm_slides || exit 9
DECK=videos/machine-learning/03_ridger_regression_gradient_descent
QA=$DECK/recreated_pptx/qa/slide_015
NAME="${1:?usage: dispatch_7_crop.sh <eq_stack|pinkbox|peachbox|deriv_stack|solution>}"
case "$NAME" in
  eq_stack)    REGION="three-line J(W) objective-function expansion stack in the cream rect (each line ends with an inline green +1/2 lambda W-transpose-W term)" ;;
  pinkbox)     REGION="the red-bordered callout box: dJ/dW = 0 identity and the 'Get Best W that minimizes the Objective Function J(W)' sentence (the W of Best W is red in the original)" ;;
  peachbox)    REGION="the peach Remember box: red bold 'Remember' label and the dW-transpose-W/dW = 2W identity with green W" ;;
  deriv_stack) REGION="the two dJ/dW gradient simplification lines ending in +lambda W and +lambda I W" ;;
  solution)    REGION="the green result box with the closed-form W = (X-transpose-X + lambda I)^-1 X-transpose-Y solution" ;;
  *) echo "unknown region $NAME"; exit 2 ;;
esac

PAYLOAD=$(sed "s/slide NNN/slide 015/g" $DECK/recreated_pptx/qa/rejudge_20261027/payload_B.tmpl)
PMD5=$(printf '%s' "$PAYLOAD" | md5sum | cut -d' ' -f1)
echo "payload_B(015) md5=$PMD5"
[ "$PMD5" = "110aa1c75d36a5972ee62043a5ab2da3" ] || { echo "PAYLOAD MD5 MISMATCH"; exit 8; }

timeout 1700 bash scripts/16_vision_gate.sh python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  "$QA/crop_6_${NAME}_render.png" \
  "$QA/crop_6_${NAME}_orig.png" \
  --view "Slide 015 zoomed crop ${NAME} — render vs original at matched effective scale (attempt 7)" \
  --capture "IMG1=zoomed crop of the 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: ${REGION}" \
  --thinking high --max-tokens 65536 \
  --timeout 600 --rounds 1 --tries 1 \
  --transcript "$QA/crop_7_${NAME}_judge.txt" \
  -p "$PAYLOAD"
echo "CROP $NAME DONE rc=$?"
