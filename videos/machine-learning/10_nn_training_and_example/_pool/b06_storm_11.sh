#!/usr/bin/env bash
# b06 storm-clause retry loop for slide 011 comparison judge.
# Each retry: sleep 120s then one judge call. Bails early on a real verdict
# or on a non-storm (content) error. Transport-class = 429/502/504/timeout/Connection.
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
cd "$NS"
PROMPT="$(cat judge_template.txt)"
G="python3 /home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py"

run_j() { # $1 = attempt number
  timeout 600 env VISION_SLOTS=3 bash _pool/vision_gate.sh \
    $G comparison qa/slide011/rejudge/_attempt2/render-1.png unique_slides/slide_011.jpg \
    --view "Slide 011 recreation render vs original lecture frame" \
    --capture "13.33x7.5in slide, 150dpi render (2000x1125px) vs 960x540px original frame" \
    -p "$PROMPT" --timeout 420 --rounds 1 --tries 1 \
    > "qa/slide011/rejudge/judge_attempt_$1.txt" 2>&1
  local rc=$?
  cp "qa/slide011/rejudge/judge_attempt_$1.txt" "qa/slide_011_judge_attempt$1.txt"
  echo "judge 011 attempt_$1 rc=$rc bytes=$(wc -c < qa/slide011/rejudge/judge_attempt_$1.txt) $(date +%T)" \
    >> _pool/b06_judge_11.status
}

for N in 9 10 11; do
  echo "=== storm retry attempt $N $(date +%T)" >> _pool/b06_storm.status
  sleep 120
  run_j "$N"
  F="qa/slide011/rejudge/judge_attempt_$N.txt"
  if grep -q 'FINAL VERDICT' "$F"; then
    echo "VERDICT attempt $N $(date +%T)" >> _pool/b06_storm.status
    exit 0
  fi
  if ! grep -qE '429|502|504|timeout|timed out|Connection|reset|HangError' "$F"; then
    echo "NONSTORM attempt $N $(date +%T)" >> _pool/b06_storm.status
    exit 0
  fi
  echo "TRANSPORT attempt $N $(date +%T)" >> _pool/b06_storm.status
done
echo "STORM-EXHAUSTED $(date +%T)" >> _pool/b06_storm.status
