#!/usr/bin/env bash
# b07: retry judge for slide 14 (attempt_1 upstream 400). Storm clause:
# sleep 120 between tries, max 4 extra attempts. Banked per attempt.
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
SKILL=/home/codespace/ai_llm_slides/.agents/skills/image-analysis
cd "$NS"
PROMPT="$(cat judge_template.txt)"

for k in 2 3 4 5 6; do
  sleep 120
  ./_pool/vision_gate.sh timeout 540 \
    python3 "$SKILL/scripts/analyze_image.py" comparison \
    qa/slide014/b07/render-1.png unique_slides/slide_014.jpg \
    --view "Slide 14 recreation render vs original lecture frame" \
    --capture "13.33x7.5in slide, 150dpi render (2001x1125px) vs 960x540px original frame" \
    -p "$PROMPT" --timeout 420 --rounds 1 --tries 1 \
    > "qa/slide014/b07/judge_attempt_${k}.txt" 2>&1
  rc=$?
  echo "slide 14 attempt $k rc=$rc bytes=$(wc -c < qa/slide014/b07/judge_attempt_${k}.txt) $(date +%F\ %T)" >> _pool/b07_judge.log
  if grep -aq "FINAL VERDICT" "qa/slide014/b07/judge_attempt_${k}.txt"; then
    echo "slide 14 attempt $k has verdict, stopping" >> _pool/b07_judge.log
    break
  fi
done
echo "b07 judge14 retry loop done $(date +%F\ %T)" >> _pool/b07_judge.log
