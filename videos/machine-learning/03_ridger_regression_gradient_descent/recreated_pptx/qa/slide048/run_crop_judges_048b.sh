#!/bin/bash
# Zoomed crop-pair judges for slide 048 attempt 10 (render_9) — one crop at a time.
# Usage: bash run_crop_judges_048.sh top_band|aug_iter|calc_panel
# crop_9 pairs were cut from render_9 (verified pixel-identical to the fresh
# render of the current pptx). Payload = frozen Template B (slide 048).
set -u
ROOT="/home/ahmed/Projects/ai_llm_slides"
QA="$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide048"
NAME="${1:?crop name required}"
DESC=""
case "$NAME" in
  top_band)   DESC="top band: x1..x6 input table with Initial W column, red REPEAT band, class row, Check classes of Z1Z2Z3 grid" ;;
  aug_iter)   DESC="augmented 3x6 vector table with red Iteration 1 box" ;;
  calc_panel) DESC="right calculation panel: six update-weight equation rows with red arrows" ;;
  *) echo "unknown crop $NAME"; exit 2 ;;
esac

cd "$ROOT"
LOAD=$(pgrep -c -f '[a]nalyze_image.py' || true)
echo "[gate law] fleet analyze_image.py procs = $LOAD"
if [ "${LOAD:-0}" -ge 8 ]; then echo "FLEET >=8 — do not dispatch; heartbeat, sleep 240, re-probe"; exit 3; fi

scripts/16_vision_gate.sh timeout 1700 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide048/crop_10_${NAME}_render.png" \
  "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide048/crop_10_${NAME}_orig.png" \
  --view "Slide 048 zoomed crop ${NAME} — render vs original at matched scale (attempt 10)" \
  --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: ${DESC}" \
  --thinking high --max-tokens 65536 \
  --timeout 1200 --rounds 1 --tries 1 \
  --transcript "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide048/crop_10_${NAME}_judge.txt" \
  -p "$(cat "$QA/crop_1_calc_panel_prompt.txt")" 2>&1 | tail -5
