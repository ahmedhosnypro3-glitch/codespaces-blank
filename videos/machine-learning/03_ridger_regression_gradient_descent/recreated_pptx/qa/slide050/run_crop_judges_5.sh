#!/bin/bash
# Procedure B dispatcher for slide 050 attempt 5 — one crop at a time, gate law enforced.
# Usage: bash run_crop_judges_5.sh caption|mathzone|tableeq|pinkbox|chart|redstop
set -u
ROOT="/worksp""aces/codespaces-blank/ai_llm_slides"
QA="$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide050"
NAME="${1:?crop name required}"
DESC=""
case "$NAME" in
  caption)  DESC="L4 key caption band below the math lines: C1 positive / C2 negative / Zero is unaccepted in red / blue / green / black" ;;
  mathzone) DESC="math zone inside the navy box: Initial W = (4/-2) stacked vector, REPEAT using Step eta = 1, Check classes of, Z1 Z2 Z3 mini-table" ;;
  tableeq)  DESC="top navy box: x1..x6 data table with two value rows plus the red/blue class row, the math zone and the L4 caption" ;;
  pinkbox)  DESC="pink weight box top-right with the underlined W = (5/-1) stacked column vector" ;;
  chart)    DESC="scatter chart: red-bordered white panel, 0..8 x ticks and 0..7 y ticks, descending red decision line with arrow, blue squares, magenta diamonds, red triangle, red origin blob, +ve annotation" ;;
  redstop)  DESC="red Iteration 2 box plus the No change in W and Stop Iterations text" ;;
  *) echo "unknown crop $NAME"; exit 2 ;;
esac

cd "$ROOT"
LOAD=$(pgrep -c -f analyze_image.py || true)
echo "[gate law] fleet analyze_image.py procs = $LOAD"
if [ "$LOAD" -ge 8 ]; then echo "FLEET >=8 — do not dispatch; heartbeat, sleep 240, re-probe"; exit 3; fi

scripts/16_vision_gate.sh timeout 1700 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide050/crop_5_${NAME}_render.png" \
  "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide050/crop_5_${NAME}_orig.png" \
  --view "Slide 050 zoomed crop ${NAME} — render vs original at matched scale (attempt 5)" \
  --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: ${DESC}" \
  --thinking high --max-tokens 65536 \
  --timeout 600 --rounds 1 --tries 1 \
  --transcript "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide050/crop_5_${NAME}_judge.txt" \
  -p "$(cat "$QA/judge_payload_B_5.txt")" 2>&1 | tail -5
