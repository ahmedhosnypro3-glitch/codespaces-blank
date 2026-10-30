#!/usr/bin/env bash
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
cd "$NS"
PROMPT="$(cat judge_template.txt)"
./_pool/vision_gate.sh timeout 540 \
  python3 /home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py \
  comparison qa/slide003/rejudge/r2/render-1.png unique_slides/slide_003.jpg \
  --view "Slide 003 recreation render vs original lecture frame" \
  --capture "13.33x7.5in slide, 150dpi render (2001x1125px) vs 960x540px original frame" \
  -p "$PROMPT" --timeout 420 --rounds 1 --tries 1 \
  > qa/slide003/rejudge/r2/judge_attempt_1.txt 2>&1 &
P1=$!
sleep 15
./_pool/vision_gate.sh timeout 540 \
  python3 /home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py \
  comparison qa/slide004/rejudge/r2/render-1.png unique_slides/slide_004.jpg \
  --view "Slide 004 recreation render vs original lecture frame" \
  --capture "13.33x7.5in slide, 150dpi render (2001x1125px) vs 960x540px original frame" \
  -p "$PROMPT" --timeout 420 --rounds 1 --tries 1 \
  > qa/slide004/rejudge/r2/judge_attempt_1.txt 2>&1 &
P2=$!
wait $P1 $P2
echo "judges done rc1=$? $(date -u +%T)"
