#!/bin/bash
# Usage: dispatch_crops_r3.sh toppanel|augtable|calcs
set -u
cd /home/ahmed/Projects/ai_llm_slides
DECK=videos/machine-learning/03_ridger_regression_gradient_descent
D=$DECK/recreated_pptx/qa/slide045
NAME="${1:?region required}"
n=$(pgrep -c -f "[a]nalyze_image.py" || true)
echo "[crop3-$NAME] $(date -u +%H:%M:%S) analyzer procs=$n"
if [ "${n:-0}" -ge 8 ]; then echo "GATE BUSY"; exit 75; fi
exec timeout 1700 bash scripts/16_vision_gate.sh python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  "$D/crop_1_r3_${NAME}_render.png" \
  "$D/crop_1_r3_${NAME}_orig.png" \
  --view "Slide 045 zoomed crop ${NAME} — render vs original at matched scale (attempt 4 leg)" \
  --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale" \
  --thinking high --max-tokens 65536 --timeout 1200 --rounds 1 --tries 1 \
  --transcript "$D/crop_1_r3_${NAME}_judge.txt" \
  -p "$(cat "$D/crop_prompt_1_r2_${NAME}.txt")"
