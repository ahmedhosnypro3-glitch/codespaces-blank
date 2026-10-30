#!/usr/bin/env bash
set -u
SKILL=/home/codespace/.agents/skills/image-analysis
VID=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
PROMPT="$(cat $VID/judge_template.txt)"
cd "$SKILL"
run_judge() {
  n="$1"
  timeout 540 python3 analyze_image/analyze_image.py comparison \
    "$VID/qa/slide${n}/rejudge/render-1.png" \
    "$VID/unique_slides/slide_${n}.jpg" \
    --view "Slide $n recreation render vs original lecture frame" \
    --capture "13.33x7.5in slide, 150dpi render (2000x1125px) vs 960x540px original frame" \
    -p "$PROMPT" --timeout 420 --rounds 1 --tries 1 \
    > "$VID/qa/slide${n}/rejudge/judge_attempt_2.txt" 2>&1
  echo "slide $n exit=$?"
}
run_judge 007 &
run_judge 008 &
sleep 15
run_judge 010 &
wait
