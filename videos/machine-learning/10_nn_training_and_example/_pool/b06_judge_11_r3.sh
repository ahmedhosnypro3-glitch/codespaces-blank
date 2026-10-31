#!/usr/bin/env bash
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
cd "$NS"
PROMPT="$(cat judge_template.txt)"
# image1 = recreation render, image2 = original (frozen template: "first = image 1 = recreation render")
timeout 600 env VISION_SLOTS=3 bash _pool/vision_gate.sh \
  python3 /home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py \
  comparison qa/slide011/rejudge/_attempt2/render-1.png unique_slides/slide_011.jpg \
  --view "Slide 011 recreation render vs original lecture frame" \
  --capture "13.33x7.5in slide, 150dpi render (2000x1125px) vs 960x540px original frame" \
  -p "$PROMPT" --timeout 420 --rounds 1 --tries 1 \
  > qa/slide011/rejudge/judge_attempt_8.txt 2>&1
rc=$?
cp qa/slide011/rejudge/judge_attempt_8.txt qa/slide_011_judge_attempt8.txt
echo "judge 011 attempt_8 rc=$rc bytes=$(wc -c < qa/slide011/rejudge/judge_attempt_8.txt) $(date +%T)" \
  >> _pool/b06_judge_11.status
