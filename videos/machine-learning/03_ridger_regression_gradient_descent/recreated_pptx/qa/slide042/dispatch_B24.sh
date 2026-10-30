#!/usr/bin/env bash
# Slide 042 leg B — ONE zoomed crop-pair certificate (Template B), attempt 24.
# Usage: dispatch_B24.sh <name>   (name in: stack tl_table lm_table topright legend initial_w)
# Payload: crop_24_<name>_prompt.txt (== protocol Template B line 117, NNN->042 only).
# Walls: --timeout 1200 inside `timeout 1700`, --thinking high --max-tokens 65536, --rounds 1 --tries 1.
set -u
NAME="${1:?usage: dispatch_B24.sh <name>}"
cd /home/ahmed/Projects/ai_llm_slides || exit 1
export TMPDIR=/home/ahmed/Projects/ai_llm_slides/scratch/tmp
export VIDEO=machine-learning/03_ridger_regression_gradient_descent
GATE="scripts/16_vision_gate.sh"
PY=".agents/skills/image-analysis/scripts/analyze_image.py"
QA="videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide042"
W="kimi-s6-FRESH-1792954337"

case "$NAME" in
  stack)     DESC="the six-box right computation stack: d(x_i) inner-product computations, update/keep actions, W result equations" ;;
  tl_table)  DESC="top-left vector table: x1..x6 columns with two digit bands, C1/C2 class row, red arrow" ;;
  lm_table)  DESC="left-middle 'Ugmented Vectors ( from Top )' table: six columns x three digit rows with per-column parens, C1/C2 class row" ;;
  topright)  DESC="top-right check-classes block: caption, Z1 Z1 Z1 header, two digit rows" ;;
  legend)    DESC="colour legend row (C1 red positive, C2 blue negative, Zero green is unaccepted) with the red arrow at its left" ;;
  initial_w) DESC="top-centre Initial W matrix: bold italic underlined W =, tall black parens spanning three digit rows 4/-2/-2, red italic Step eta = 2" ;;
  *) echo "unknown crop name: $NAME"; exit 1 ;;
esac

if [ -s "$QA/crop_24_${NAME}_judge.txt" ]; then echo "CROP $NAME ALREADY BANKED — skip (never double-dispatch)"; exit 0; fi

gate_wait() {
  local tries=0
  while [ "$(pgrep -c -f analyze_image.py)" -ge 8 ]; do
    tries=$((tries+1))
    if [ "$tries" -gt 4 ]; then echo "GATE STILL BUSY after $tries backoffs — PARK (rc 42)"; exit 42; fi
    echo "GATE BUSY ($(pgrep -c -f analyze_image.py)) — backoff $tries/4 (240s)"; python3 scripts/15_progress.py heartbeat 42 "$W" || true
    sleep 240
  done
}

gate_wait
echo "DISPATCH crop_24_$NAME at $(date -Is), gate=$(pgrep -c -f analyze_image.py)"
$GATE timeout 1700 python3 $PY comparison \
  "$QA/crop_24_${NAME}_render.png" \
  "$QA/crop_24_${NAME}_orig.png" \
  --view "Slide 042 zoomed crop $NAME — render vs original at matched scale (attempt 24)" \
  --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: $DESC" \
  --thinking high --max-tokens 65536 --timeout 1200 --rounds 1 --tries 1 \
  --transcript "$QA/crop_24_${NAME}_judge.txt" \
  -p "$(cat $QA/crop_24_${NAME}_prompt.txt)"
echo "LEG B ($NAME) EXIT=$? at $(date -Is)"
