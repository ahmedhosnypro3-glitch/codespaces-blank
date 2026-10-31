#!/usr/bin/env bash
# args: <slide> <promptfile> <outfile>
V=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
cd "$V" || exit 9
S=$1; P=$2; OUT=$3
VISION_SLOTS=2 ./_pool/vision_gate.sh timeout 540 python3 -u /home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py \
  analysis "unique_slides/slide_$S.jpg" --timeout 420 --rounds 1 --tries 1 --max-tokens 24000 \
  --view "Slide $S - original lecture frame for parse verification" --capture "960x540 px, scale 1, video frame" \
  -p "$(cat "$P")" > "$OUT" 2>&1
echo "vision$S rc=$?" >> "$OUT"
