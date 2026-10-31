#!/usr/bin/env bash
# Detached single-slide parse-verification cross-check runner.
# $1 = slide number (e.g. 008), $2 = absolute path to the prompt file.
set -u
N="$1"; PROMPT="$2"
V=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/analysis/parse/adjudication/vision
cd /home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
VISION_SLOTS=2 ./_pool/vision_gate.sh timeout 900 python3 -u \
  /home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py \
  analysis "$V/png/slide_$N.png" \
  --view "Slide $N - original lecture frame, parse-verification cross-check" \
  --capture "960x540 px, scale 1, video frame" \
  -p "$(cat "$PROMPT")" \
  --timeout 420 --rounds 2 --tries 2 --max-tokens 24000 \
  > "$V/slide_$N.vision.txt" 2>&1
echo "EXIT_$N=$?" >> "$V/run_status.log"
