#!/usr/bin/env bash
set -u
cd /home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
PROMPT="$(cat judge_template.txt)"
./_pool/vision_gate.sh timeout 540 \
  python3 /home/codespace/.agents/skills/image-analysis/scripts/analyze_image.py \
  comparison qa/slide011/rejudge/_attempt2/render-1.png unique_slides/slide_011.jpg \
  --view "Slide 011 recreation render vs original lecture frame" \
  --capture "13.33x7.5in slide, 150dpi render (2000x1125px) vs 960x540px original frame" \
  -p "$PROMPT" --timeout 420 --rounds 1 --tries 1 \
  > qa/slide011/rejudge/judge_attempt_4.txt 2>&1
echo "rc=$? $(date +%T)" >> _pool/b06_judge_11.status
