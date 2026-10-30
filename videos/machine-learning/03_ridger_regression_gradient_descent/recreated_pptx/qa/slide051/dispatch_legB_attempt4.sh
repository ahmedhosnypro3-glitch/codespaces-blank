#!/usr/bin/env bash
# Leg B — zoomed crop-pair certificates for slide 051, attempt 4.
# Payload: Template B from shared_patterns/judge_protocol_03.md line 117, byte-frozen
# as crop_attempt_2_promptB.txt (md5 6ae2c27e0ac3c7f3716ae50f823ebb25, 1913 chars).
# Crops cut from render_3.png at matched effective scale:
#   render  x*2001/960 y*1125/540 ; original LANCZOS-upscaled to the same output size.
# Walls (orchestrator override): analyzer --timeout 1200, gate 1650, outer timeout 1700.
# Gate check before EACH crop: pgrep -c -f analyze_image.py must be < 8.
set -u
cd "/home/ahmed/Projects/ai_llm_slides"
DECK="videos/machine-learning/03_ridger_regression_gradient_descent"
D="$DECK/recreated_pptx/qa/slide051"
PROMPT="$(cat "$D/crop_attempt_2_promptB.txt")"

gate_ok() {
  local n
  n=$(pgrep -c -f analyze_image.py || true)
  echo "[legB4] $(date -u +%H:%M:%S) analyzer procs=$n"
  if [ "${n:-0}" -ge 8 ]; then echo "[legB4] GATE BUSY"; return 1; fi
  return 0
}

judge() {
  local NAME="$1" DESC="$2"
  echo "### crop $NAME"
  gate_ok || { echo "[legB4] SKIPPING $NAME — gate busy ($(pgrep -c -f analyze_image.py || echo ?))"; return 75; }
  timeout 1700 bash scripts/16_vision_gate.sh python3 \
    .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    "$D/crop_4_${NAME}_render.png" \
    "$D/crop_4_${NAME}_orig.png" \
    --view "Slide 051 zoomed crop ${NAME} — render vs original at matched scale (attempt 4)" \
    --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: ${DESC}" \
    --thinking high --max-tokens 65536 \
    --timeout 1200 --rounds 1 --tries 1 \
    --transcript "$D/crop_4_${NAME}_judge.txt" \
    -p "$PROMPT"
}

NAME="${1:-all}"
case "$NAME" in
  mats) judge mats "top band: left sample 2x6 bracket matrix, centre Initial W vector + Step eta + legend, right Z test bracket matrix" ;;
  aug)  judge aug "augmented-vectors 3x6 bracket matrix with C1/C2 class row" ;;
  dec)  judge dec "three decision rows d(Z1)/d(Z2)/d(Z3) with green weight-vector brackets and result chains" ;;
  all)
    judge dec "three decision rows d(Z1)/d(Z2)/d(Z3) with green weight-vector brackets and result chains" || exit 75
    judge mats "top band: left sample 2x6 bracket matrix, centre Initial W vector + Step eta + legend, right Z test bracket matrix" || exit 75
    judge aug "augmented-vectors 3x6 bracket matrix with C1/C2 class row" || exit 75
    ;;
esac
echo "### legB4 done"
