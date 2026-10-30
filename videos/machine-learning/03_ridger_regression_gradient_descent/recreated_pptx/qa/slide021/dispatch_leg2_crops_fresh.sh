#!/usr/bin/env bash
# LEG 2 (Procedure B) — zoomed crop-pair certificates, slide 021 attempt 10 (render_10.png)
# Fresh lane copy of dispatch_leg2_crops.sh. Owner: WID (default w021-fresh-20261024).
# Only the four legs that were MISSING when this was banked; top_table_eq is already PASS.
# Payload byte-for-byte from judge_protocol_03.md Template B (banked: crop_prompt_template_10.txt,
# 1915 chars, NNN->021 already substituted; region description goes in --capture).
# Cut pairs (matched effective scale 2.0833, verified output_px/frame_px equal on both axes):
#   top_table_eq  x88..322  y126..232  490x223
#   top_chain     x332..802 y182..218  981x77
#   mid_table_eq  x80..322  y290..402  506x236
#   mid_chain     x332..892 y348..382  1168x73
#   bot_eq_table  x148..642 y450..519  1032x145
set -u
ROOT="/workspaces/codespaces-blank/ai_llm_slides"
V="videos/machine-learning/03_ridger_regression_gradient_descent"
QADIR="$ROOT/$V/recreated_pptx/qa/slide021"
# Owner of the lane's DB claim; a resume lane overrides WID after its own `claim 21 <id>`.
WID="${WID:-w021-fresh-20261024}"
# Which legs to attempt, plus how long to wait for a gate window before parking honestly.
SLUGS="${SLUGS:-top_chain mid_table_eq mid_chain bot_eq_table}"
POLL_MAX="${POLL_MAX:-7200}"
POLL_EVERY="${POLL_EVERY:-240}"
PAYLOAD="$(cat "$QADIR/crop_prompt_template_10.txt")"
cd "$ROOT"
hb () {
  cd "$ROOT" && VIDEO=machine-learning/03_ridger_regression_gradient_descent \
    python3 scripts/15_progress.py heartbeat 21 "$WID" >/dev/null 2>&1
  cd "$ROOT"
}
run_crop () {
  local slug="$1" desc="$2"
  hb
  echo "=== crop $slug ==="
  local tf="$QADIR/crop_10_${slug}_judge.txt"
  if [ -f "$tf" ] && grep -q "FINAL VERDICT:" "$tf" 2>/dev/null; then
    echo "SKIP $slug — already carries a verdict: $(grep -o 'FINAL VERDICT:.*' "$tf" | tail -1 | cut -c1-60)"
    return 0
  fi
  pgrep_count="$(pgrep -c -f analyze_image.py || true)"
  if [ "${pgrep_count:-0}" -ge 8 ]; then
    echo "GATE: $pgrep_count analyze_image.py running (>=8) — NOT dispatching $slug; park and re-probe later."
    return 99
  fi
  cd "$ROOT" && VIDEO=machine-learning/03_ridger_regression_gradient_descent \
    python3 scripts/15_progress.py heartbeat 21 "$WID" >/dev/null 2>&1
  cd "$ROOT"
  scripts/16_vision_gate.sh timeout 1700 python3 \
    .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    "$V/recreated_pptx/qa/slide021/crop_10_${slug}_render.png" \
    "$V/recreated_pptx/qa/slide021/crop_10_${slug}_orig.png" \
    --view "Slide 021 zoomed crop ${slug} — render vs original at matched scale (attempt 10)" \
    --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: ${desc}" \
    --thinking high --max-tokens 65536 \
    --timeout 1200 --rounds 1 --tries 1 \
    --transcript "$V/recreated_pptx/qa/slide021/crop_10_${slug}_judge.txt" \
    -p "$PAYLOAD"
}
for slug in top_chain mid_table_eq mid_chain bot_eq_table; do
  case " $SLUGS " in *" $slug "*) ;; *) continue ;; esac
  case "$slug" in
    top_chain)    desc="the first block's determinant chain: |X^T X| = 0, two blue arrows, Singular Matrix, red italic No Inverse" ;;
    mid_table_eq) desc="the second block's left side: the (X^T X + lambda I) label, green lambda=3, the full 3x3 regularized matrix, and the three FDFD96 highlight bands on the 17/43/95 diagonal" ;;
    mid_chain)    desc="the second block's determinant chain: |X^T X| = 5685, two blue arrows, Non-Singular Matrix, red italic Inverse Exists" ;;
    bot_eq_table) desc="the bottom block: the (X^T X + lambda I)^-1 expression, the long blue arrow, and the 3x3 inverse matrix table of decimals" ;;
  esac
  t0=$(date +%s)
  while :; do
    el=$(( $(date +%s) - t0 ))
    c="$(pgrep -c -f analyze_image.py || true)"
    if [ "${c:-0}" -lt 8 ]; then break; fi
    hb
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] GATE pgrep=$c (>=8) for $slug — heartbeat sent, sleeping ${POLL_EVERY}s (waited ${el}s)"
    [ "$el" -ge "$POLL_MAX" ] && { echo "POLL CAP ${el}s for $slug — honest park, NOT dispatched"; exit 42; }
    sleep "$POLL_EVERY"
  done
  run_crop "$slug" "$desc" || true
done
hb
echo "ALL CROPS DONE by ${WID}"
