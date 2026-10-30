#!/usr/bin/env bash
# LEG 2 — Procedure B zoomed crop-pair certificates, slide 021 attempt 10 (render_10.png)
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
PAYLOAD="$(cat "$QADIR/crop_prompt_template_10.txt")"
cd "$ROOT"
run_crop () {
  local slug="$1" desc="$2"
  echo "=== crop $slug ==="
  pgrep_count="$(pgrep -c -f analyze_image.py || true)"
  if [ "${pgrep_count:-0}" -ge 8 ]; then
    echo "GATE: $pgrep_count analyze_image.py running (>=8) — NOT dispatching $slug; park and re-probe later."
    return 99
  fi
  scripts/16_vision_gate.sh timeout 1700 python3 \
    .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    "$V/recreated_pptx/qa/slide021/crop_10_${slug}_render.png" \
    "$V/recreated_pptx/qa/slide021/crop_10_${slug}_orig.png" \
    --view "Slide 021 zoomed crop ${slug} — render vs original at matched scale (attempt 10)" \
    --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: ${desc}" \
    --thinking high --max-tokens 65536 \
    --timeout 600 --rounds 1 --tries 1 \
    --transcript "$V/recreated_pptx/qa/slide021/crop_10_${slug}_judge.txt" \
    -p "$PAYLOAD"
}
run_crop top_table_eq "the top-left of the first block: the red X^T X label equation and the full 3x3 singular matrix table with its gridlines"
rc=$?
[ $rc -eq 99 ] && exit 0
run_crop top_chain   "the first block's determinant chain: |X^T X| = 0, two blue arrows, Singular Matrix, red italic No Inverse" || true
run_crop mid_table_eq "the second block's left side: the (X^T X + lambda I) label, green lambda=3, the full 3x3 regularized matrix, and the three FDFD96 highlight bands on the 17/43/95 diagonal" || true
run_crop mid_chain   "the second block's determinant chain: |X^T X| = 5685, two blue arrows, Non-Singular Matrix, red italic Inverse Exists" || true
run_crop bot_eq_table "the bottom block: the (X^T X + lambda I)^-1 expression, the long blue arrow, and the 3x3 inverse matrix table of decimals" || true
