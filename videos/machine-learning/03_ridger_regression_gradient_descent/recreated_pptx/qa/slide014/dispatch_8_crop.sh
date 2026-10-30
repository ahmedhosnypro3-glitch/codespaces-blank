#!/bin/bash
# Slide 014 — attempt-8 Procedure B crop-pair judge (Template B), one region per call:
#   dispatch_8_crop.sh <bands|vectors|final>
# Payload = the banked payload_B_7 files, byte-verified identical to the frozen
# Template B payload (md5 978be75de7b83501d09f8f0c5576cbee; only legal sub slide NNN->slide 014).
# Crops cut fresh from render_8 by create_crops_8.py at matched effective scale.
cd /home/ahmed/Projects/ai_llm_slides || exit 9
NAME="${1:?usage: dispatch_8_crop.sh <bands|vectors|final>}"
case "$NAME" in
  vectors) REGION="two vector-definition boxes: left 'Original Labels / from Training Samples' text beside a red y column vector in maroon-bordered box; right 'Predicted Labels / from Model' text beside a blue y-hat column vector with bold underlined X W" ;;
  bands)   REGION="two navy-ruled yellow bands: 'Y-hat=Y and ||W|| is minimum ... This is called Ridge Regularization' and the 'Objective function J(W) = Loss(X,Y,W) + lambda R(W) (lambda is a weighting factor)' line" ;;
  final)   REGION="final pale-cyan objective-function band with the J(W) loss-plus-regularization expansion (bold underlined Y, squared terms, lambda W-transpose W)" ;;
  *) echo "unknown region $NAME"; exit 2 ;;
esac
LOAD=$(pgrep -c -f analyze_image.py); echo "gate load: $LOAD"
[ "$LOAD" -lt 8 ] || { echo "GATE CLOSED"; exit 7; }
bash scripts/16_vision_gate.sh timeout 1700 python3 .agents/skills/image-analysis/scripts/analyze_image.py comparison videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide014/crop_8_${NAME}_render.png videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide014/crop_8_${NAME}_orig.png --view "Slide 014 zoomed crop ${NAME} — render vs original at matched scale (attempt 8)" --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: ${REGION}" --thinking high --max-tokens 65536 --timeout 1200 --rounds 1 --tries 1 --transcript videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide014/crop_8_${NAME}_judge.txt -p "$(cat videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide014/payload_B_7_bands.txt)"
echo "CROP $NAME DONE rc=$?"
