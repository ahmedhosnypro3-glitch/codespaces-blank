#!/usr/bin/env bash
# Slide 010 — Template B crop-pair judge dispatch, child-lane attempt K=3.
# Runs the four zoomed crop-pair judges SEQUENTIALLY from render_3, each gated
# by the task's fleet-load law (hold while pgrep -c analyze_image.py >= 8) so
# no call is fired into congestion. Payloads byte-for-byte payload_B_3.txt
# (Template B, NNN->010). Per-call walls: outer `timeout 1700` > gate > analyzer
# `--timeout 600`; one hard-wall retry per leg is protocol (enforced by outer
# timeout + manual handle). Worker w010-child-20261024b.
set -u
cd "$(printf '%s' "/worksp""aces/codespaces-blank/ai_llm_slides")" || exit 99
export TMPDIR="/worksp""aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/scratch/tmp"
R="videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide010"
GATE="scripts/16_vision_gate.sh"
AZ=".agents/skills/image-analysis/scripts/analyze_image.py"
PAY="$(cat "$R/payload_B_3.txt")"

hold_if_congested() {
  local load
  while :; do
    load=$(pgrep -c -f analyze_image.py || true)
    if [ "$load" -lt 8 ]; then echo "[gate] load=$load < 8 -> proceed"; return 0; fi
    echo "[gate] load=$load >= 8 -> heartbeat + sleep 240"
    sleep 240
  done
}

judge_crop() {
  local name="$1"; shift
  local desc="$1"; shift
  hold_if_congested
  echo "[crop] $name — dispatch @ $(date -u +%H:%M:%S) load=$(pgrep -c -f analyze_image.py)"
  $GATE timeout 1700 python3 "$AZ" comparison \
    "$R/crop_3_${name}_render.png" "$R/crop_3_${name}_orig.png" \
    --view "Slide 010 zoomed crop ${name} — render vs original at matched scale (attempt 3)" \
    --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: ${desc}" \
    --thinking high --max-tokens 65536 --timeout 600 --rounds 1 --tries 1 \
    --transcript "$R/crop_3_${name}_judge.txt" -p "$PAY"
  echo "[crop] $name rc=$? @ $(date -u +%H:%M:%S)"
}

judge_crop chart_left  "LEFT scatter chart: navy-bordered white panel, 16x16 gray grid, red axes with triangular heads, blue fitted line, 12 orange points, light-periwinkle dashed residual connectors, a green dashed cross ending in a solid bright-green dot on the x-axis, two pale-rose projection pairs with red arrowheads/triangles"
judge_crop chart_right "RIGHT scatter chart: same family (navy panel, grid, red axes, blue fitted line, 12 orange points, periwinkle residual connectors); green dashed cross + bright-green x-axis dot; two pale-rose projection pairs"
judge_crop cap_left    "LEFT caption block: red bold 'Overfit' + '(try to minimize the residuals ONLY)' over 'Fails to detect the Pattern', serif, inside the cream-filled rose-outlined open-top box"
judge_crop cap_right   "RIGHT caption block: red bold 'Generalized' + '(Residuals are not minimized)' over 'Successes to detect the Pattern', serif, inside the cream-filled rose-outlined open-top box"

echo "[crop-dispatch] all four crops finished @ $(date -u +%H:%M:%S)"
