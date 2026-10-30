#!/usr/bin/env bash
# Procedure B crop-pair judge legs for slide 044, attempt 2 (render_2.png).
# Payloads are byte-for-byte from shared_patterns/judge_protocol_03.md Template B
# with only NNN/K/NAME/region-description substituted (regenerated, not the
# corrupted banked copies). One call per region, all wrapped per the wall law.
set -u
cd /home/ahmed/Projects/ai_llm_slides || exit 2
V="videos/machine-learning/03_ridger_regression_gradient_descent"
Q="$V/recreated_pptx/qa/slide044"

for NAME in lefttables eqstack centretext; do
  PAY="$(cat "$Q/judgepayload_legs_B_${NAME}.txt")"
  bash scripts/16_vision_gate.sh timeout 1700 python3 \
    .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    "$Q/crop_2_${NAME}_render.png" \
    "$Q/crop_2_${NAME}_orig.png" \
    --view "Slide 44 zoomed crop 2_${NAME} — render vs original at matched scale (attempt 2)" \
    --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale" \
    --thinking high --max-tokens 65536 \
    --timeout 1200 --rounds 1 --tries 1 \
    --transcript "$Q/legB_${NAME}_attempt_1.txt" \
    -p "$PAY" > "$Q/legB_${NAME}_stdout.txt" 2>&1
  echo "crop ${NAME}: rc=$?"
done
