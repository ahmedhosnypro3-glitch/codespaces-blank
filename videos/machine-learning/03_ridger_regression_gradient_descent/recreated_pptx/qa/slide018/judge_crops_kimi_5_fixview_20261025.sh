#!/usr/bin/env bash
# Slide 018 Procedure-B crop-pair judges, attempt K=5 paren-refit re-cert
# (S22 fresh carrier, 2026-10-25) — corrected copy of qa/slide018/judge_crops_kimi_5.sh
# (that staged script carried slide 017's --view label from a copy-paste; the
# --view text now says Slide 018). Payloads, capture descs, legs and walls are
# unchanged from the staged script. test + mark certificates are KEPT from the
# certified K=1/K=4 base with the banked identity proofs
# (crop5_test_mark_identity_proof.txt: mark 0-px identical; test 110-px sliver
# confined to the fixed band-1 paren top, covered by the fresh band legs).
#
# Run the gate-law pgrep check (<8) before EACH leg; one leg per dispatch.
set -u
export TMPDIR=/home/ahmed/Projects/ai_llm_slides/scratch/tmp
cd /home/ahmed/Projects/ai_llm_slides
QA=videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide018

NAME="${1:?usage: judge_crops_kimi_5_fixview_20261025.sh <wbox|band1|band2|band3>}"
# gate law: pgrep < 8 required before EVERY call.
COUNT=$(pgrep -c -f analyze_image.py || true)
if [ "${COUNT:-99}" -ge 8 ]; then
  echo "=== GATE BUSY (analyze_image.py count=${COUNT}) — not dispatching leg ${NAME} ==="
  exit 75
fi
DESC=$(python3 -c "import json,sys; print(json.load(open('$QA/region_descs_5.json'))['$NAME'])")
scripts/16_vision_gate.sh timeout 1700 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  $QA/crop_5_${NAME}_render.png \
  $QA/crop_5_${NAME}_orig.png \
  --view "Slide 018 zoomed crop ${NAME} — render vs original at matched scale (attempt 5)" \
  --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: ${DESC}" \
  --thinking high --max-tokens 65536 \
  --timeout 1200 --rounds 1 --tries 1 \
  --transcript $QA/crop_5_${NAME}_judge.txt \
  -p "$(cat $QA/crop_5_${NAME}_judge_prompt_5.txt)"
echo "=== crop leg ${NAME} finished rc=$? ==="
