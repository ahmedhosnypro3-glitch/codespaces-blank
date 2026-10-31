#!/usr/bin/env bash
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
cd "$NS" || exit 1
SK=/home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py
PROMPT="$(cat judge_template.txt)"
CAP="13.33x7.5in slide, 150dpi render (2001x1125px) vs 960x540px original frame"
K=${1:-2}
./_pool/vision_gate.sh timeout 540 python3 "$SK" comparison qa/slide024/attempt4/render-1.png unique_slides/slide_024.jpg \
  --view "Slide 024 recreation render vs original lecture frame" --capture "$CAP" \
  -p "$PROMPT" --timeout 420 --rounds 1 --tries 1 > qa/slide024/attempt4/judge_attempt_${K}.txt 2>&1
echo "$(date +%T) rc=$? bytes=$(wc -c < qa/slide024/attempt4/judge_attempt_${K}.txt)" >> _pool/b12_judge.status
grep -i "FINAL VERDICT" qa/slide024/attempt4/judge_attempt_${K}.txt >> _pool/b12_judge.status 2>&1
