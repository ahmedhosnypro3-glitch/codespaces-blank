#!/usr/bin/env bash
set -u
cd /home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
PROMPT="$(cat judge_template.txt)"
run_judge() { # $1=slide NNN, $2=render png, $3=attempt file suffix
  ./_pool/vision_gate.sh timeout 540 \
    python3 /home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py \
    comparison "$2" "unique_slides/slide_$1.jpg" \
    --view "Slide $1 recreation render vs original lecture frame" \
    --capture "13.33x7.5in slide, 150dpi render (2000x1125px) vs 960x540px original frame" \
    -p "$PROMPT" --timeout 420 --rounds 1 --tries 1 \
    > "qa/slide$1/rejudge/judge_$3.txt" 2>&1
  grep -q 'FINAL VERDICT' "qa/slide$1/rejudge/judge_$3.txt" && return 0
  grep -qE '429|rate.?limit' "qa/slide$1/rejudge/judge_$3.txt" || return 0  # real verdict or hard error: stop
  return 1
}
for k in 6 7 8 9; do
  echo "=== slide 011 attempt $k $(date +%T)" >> _pool/b06_judge_loop.status
  if run_judge 011 "qa/slide011/rejudge/_attempt2/render-1.png" "attempt_$k"; then break; fi
  sleep 120
done
for k in 4 5 6 7; do
  echo "=== slide 012 attempt $k $(date +%T)" >> _pool/b06_judge_loop.status
  if run_judge 012 "qa/slide012/rejudge/_attempt2/render-1.png" "attempt_$k"; then break; fi
  sleep 120
done
echo "done $(date +%T)" >> _pool/b06_judge_loop.status
