#!/usr/bin/env bash
# Slide 018 Procedure-B crop-pair judges, attempt K=1 (kimi-slide018, 2026-10-25).
#
# Every judge parameter is byte-identical to the frozen Template B of
# shared_patterns/judge_protocol_03.md; the -p payloads are sourced byte-for-byte
# from the banked crop_1_<name>_judge_prompt_1.txt files (reverse byte-checked),
# and the --capture region description comes from the same banked
# region_descs_1.json the payload was emitted from.
# Run the gate-law pgrep check (<8) before EACH leg.
set -u
export TMPDIR=/home/ahmed/Projects/ai_llm_slides/scratch/tmp
cd /home/ahmed/Projects/ai_llm_slides
QA=videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide018

for NAME in band1 band2 band3 test mark; do
  # gate law: pgrep < 8 required before EVERY call; abort the remaining legs
  # when the gate is busy so no leg is ever dispatched without a probe.
  COUNT=$(pgrep -c -f analyze_image.py || true)
  if [ "${COUNT:-99}" -ge 8 ]; then
    echo "=== GATE BUSY (analyze_image.py count=${COUNT}) — aborting before leg ${NAME} ==="
    exit 75
  fi
  DESC=$(python3 -c "import json,sys; print(json.load(open('$QA/region_descs_1.json'))['$NAME'])")
  scripts/16_vision_gate.sh timeout 1700 python3 \
    .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    $QA/crop_1_${NAME}_render.png \
    $QA/crop_1_${NAME}_orig.png \
    --view "Slide 018 zoomed crop ${NAME} — render vs original at matched scale (attempt 3 (crops re-cut from render_3))" \
    --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: ${DESC}" \
    --thinking high --max-tokens 65536 \
    --timeout 1200 --rounds 1 --tries 1 \
    --transcript $QA/crop_1_${NAME}_judge.txt \
    -p "$(cat $QA/crop_1_${NAME}_judge_prompt_1.txt)"
  echo "=== crop leg ${NAME} finished rc=$? ==="
done
