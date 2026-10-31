#!/usr/bin/env bash
# b07: retry judge for slide 13 (attempt_1 got upstream 400). Storm clause:
# sleep 120 between tries, max 3 extra attempts. Banked per attempt.
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
SKILL=/home/codespace/ai_llm_slides/.agents/skills/image-analysis
cd "$NS"
PROMPT="$(cat judge_template.txt)"

for k in 2 3 4; do
  sleep 120
  ./_pool/vision_gate.sh timeout 540 \
    python3 "$SKILL/scripts/analyze_image.py" comparison \
    qa/slide013/b07/render-1.png unique_slides/slide_013.jpg \
    --view "Slide 13 recreation render vs original lecture frame" \
    --capture "13.33x7.5in slide, 150dpi render (2001x1125px) vs 960x540px original frame" \
    -p "$PROMPT" --timeout 420 --rounds 1 --tries 1 \
    > "qa/slide013/b07/judge_attempt_${k}.txt" 2>&1
  rc=$?
  echo "slide 13 attempt $k rc=$rc bytes=$(wc -c < qa/slide013/b07/judge_attempt_${k}.txt) $(date +%F\ %T)" >> _pool/b07_judge.log
  if grep -aq "FINAL VERDICT" "qa/slide013/b07/judge_attempt_${k}.txt"; then
    echo "slide 13 attempt $k has verdict, stopping retries" >> _pool/b07_judge.log
    break
  fi
done
echo "b07 judge13 retry loop done $(date +%F\ %T)" >> _pool/b07_judge.log
