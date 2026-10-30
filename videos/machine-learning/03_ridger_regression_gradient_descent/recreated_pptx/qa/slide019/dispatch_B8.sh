#!/usr/bin/env bash
set -u
export TMPDIR=/workspaces/codespaces-blank/ai_llm_slides/scratch/tmp
cd /workspaces/codespaces-blank/ai_llm_slides
VID=videos/machine-learning/03_ridger_regression_gradient_descent
Q=$VID/recreated_pptx/qa/slide019
for NAME in header_strip noreg_rows table_left table_right; do
  echo "=== LEG $NAME (load $(pgrep -c -f analyze_image.py)) ==="
  scripts/16_vision_gate.sh timeout 1700 python3 \
    .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    $Q/crop_8_${NAME}_render.png $Q/crop_8_${NAME}_orig.png \
    --view "Slide 019 zoomed crop ${NAME} - render vs original at matched scale (attempt 8)" \
    --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: see worker_report_ROOT.md Procedure B table" \
    --thinking high --max-tokens 65536 --timeout 600 --rounds 1 --tries 1 \
    --transcript $Q/crop_8_${NAME}_judge.txt \
    -p "$(cat $Q/judgeB8_payload_20261024.txt)"
  echo "EXIT_${NAME}=$?"
done
