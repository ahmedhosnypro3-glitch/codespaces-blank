#!/usr/bin/env bash
# Slide 046 Procedure B — run all zoomed crop-pair judges for attempt 4.
# Each call obeys the gate law (probe pgrep -c -f analyze_image.py, sleep 240
# + re-probe while >=8) and goes through scripts/16_vision_gate.sh.
# Payloads byte-for-byte from shared_patterns/judge_protocol_03.md Template B
# (NNN=46, K=4; NAME and the region description substituted only).
set -u
cd /worksp""aces/codespaces-blank/ai_llm_slides || exit 1
D="videos/machine-learning/03_ridger_regression_gradient_descent"
Q="$D/recreated_pptx/qa/slide046"

run_crop() {
  local NAME="$1" DESC="$2"
  local n
  while :; do
    n=$(pgrep -c -f analyze_image.py || echo 0)
    if [ "${n:-0}" -ge 8 ]; then
      VIDEO=machine-learning/03_ridger_regression_gradient_descent \
        python3 scripts/15_progress.py heartbeat 46 w046-legs-20261024 >/dev/null
      echo "[gate] $n vision procs — sleeping 240 ($NAME) $(date -u +%H:%M:%S)"
      sleep 240
      continue
    fi
    break
  done
  local P
  P=$(cat "$Q/crop_4_${NAME}_payload.txt")
  echo "[crop] START $NAME $(date -u +%H:%M:%S)"
  bash scripts/16_vision_gate.sh timeout 1700 python3 \
    .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    "$Q/crop_4_${NAME}_render.png" \
    "$Q/crop_4_${NAME}_orig.png" \
    --view "Slide 046 zoomed crop ${NAME} — render vs original at matched scale (attempt 4)" \
    --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: ${DESC}" \
    --thinking high --max-tokens 65536 \
    --timeout 600 --rounds 1 --tries 1 \
    --transcript "$Q/crop_4_${NAME}_judge.txt" \
    -p "$P"
  echo "[crop] DONE $NAME rc=$? $(date -u +%H:%M:%S)"
}

run_crop topmatrix  "6 parenthesised 2-value column vectors with x1..x6 header, class row and caption"
run_crop zmatrix    "Z1 header row over three parenthesised 2-value columns"
run_crop initial    "Initial W = column vector in tall parentheses plus the red Step eta = 2 line"
run_crop yellowbox  "final-weight box with underlined W, equals sign and the 14/-4/0 column vector"
run_crop augbox     "augmented-vectors box: title, x1..x6 header, six 3-value columns, class row"
run_crop plot       "scatter plot with red border, gridlines, decision line and markers"
run_crop stopbox    "stop-iterations callout box with two-line text"
echo "[all] ALL CROP JUDGES DONE $(date -u +%H:%M:%S)"
