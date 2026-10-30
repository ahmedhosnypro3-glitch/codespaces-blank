#!/usr/bin/env bash
# scope_a18: describe slides 31 and 32 in detail (default route, no --models)
set -u
SKILL=/home/codespace/ai_llm_slides/.agents/skills/image-analysis
VID=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
cd "$SKILL" || exit 1
PROMPT="$(cat "$VID/judge_template.txt")"
mkdir -p "$VID/qa/slide031" "$VID/qa/slide032"
for n in 31 32; do
  n=$(printf "%03d" "$n")
  timeout 300 python3 scripts/analyze_image.py analysis "$VID/unique_slides/slide_${n}.jpg" \
    --timeout 240 --rounds 1 --tries 1 \
    --view "ML lecture slide $n — full content and layout map" \
    --capture "960x540 jpg frame" \
    -p "$PROMPT" > "$VID/qa/slide${n}/a18_describe.txt" 2>&1 &
  sleep 15
done
wait
echo "DESCRIBE DONE"
