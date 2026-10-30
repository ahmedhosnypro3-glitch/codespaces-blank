#!/bin/bash
set -u
cd /home/ahmed/Projects/ai_llm_slides
DECK=videos/machine-learning/03_ridger_regression_gradient_descent
D=$DECK/recreated_pptx/qa/slide048
n=$(pgrep -c -f "[a]nalyze_image.py" || true)
echo "[crop4-top_band] $(date -u +%H:%M:%S) analyzer procs=$n"
if [ "${n:-0}" -ge 8 ]; then echo "GATE BUSY"; exit 75; fi
exec timeout 1700 bash scripts/16_vision_gate.sh python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  "$D/crop_4_top_band_render.png" \
  "$D/crop_4_top_band_orig.png" \
  --view "Slide 048 zoomed crop top_band — render vs original at matched scale" \
  --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: top blue-violet box x1..x6 header table with the Initial W value row, the red REPEAT instruction, the check-classes label and 3x3 grid, the legend line" \
  --thinking high --max-tokens 65536 --timeout 1200 --rounds 1 --tries 1 \
  --transcript "$D/crop_4_top_band_judge.txt" \
  -p "$(cat "$D/crop_1_calc_panel_prompt.txt")"
