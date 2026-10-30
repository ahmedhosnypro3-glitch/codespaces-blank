#!/usr/bin/env bash
# Slide 046 Procedure B — dispatch zoomed crop-pair judges for attempt 4.
# Payloads byte-for-byte from shared_patterns/judge_protocol_03.md (Template B,
# NNN=46, K=4, NAME/region description substituted only).
# Run one crop per invocation; gate law: probe `pgrep -c -f analyze_image.py`
# before each, sleep 240 + re-probe if >=8.
set -u
cd /worksp""aces/codespaces-blank/ai_llm_slides || exit 1
D="videos/machine-learning/03_ridger_regression_gradient_descent"
Q="$D/recreated_pptx/qa/slide046"

run_crop() {
  local NAME="$1" DESC="$2"
  local n
  while :; do
    n=$(pgrep -c -f analyze_image.py || true)
    if [ "${n:-0}" -ge 8 ]; then
      VIDEO=machine-learning/03_ridger_regression_gradient_descent \
        python3 scripts/15_progress.py heartbeat 46 w046-legs-20261024 >/dev/null
      echo "[gate] $n vision procs running — sleeping 240 (crop $NAME)" >&2
      sleep 240
      continue
    fi
    break
  done
  local P
  P=$(cat "$Q/crop_4_${NAME}_payload.txt")
  echo "[crop] dispatching $NAME at $(date -u +%H:%M:%S)" >&2
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
}

run_crop "$@"
