#!/usr/bin/env bash
# b01 judge runner: slide 001 (attempt2 render) + slide 002, frozen template,
# default route, through the namespace vision gate. ≤2 concurrent.
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
SKILL=/home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py
cd "$NS" || exit 1
PROMPT="$(cat judge_template.txt)"

judge() { # $1=N  $2=render  $3=out
  local N="$1" R="$2" O="$3"
  env VISION_SLOTS=4 ./_pool/vision_gate.sh timeout 540 \
    python3 "$SKILL" comparison "$R" "unique_slides/slide_${N}.jpg" \
    --view "Slide $N recreation render vs original lecture frame" \
    --capture "13.33x7.5in slide, 150dpi render (2001x1125px) vs 960x540px original frame" \
    -p "$PROMPT" --timeout 420 --rounds 1 --tries 1 > "$O" 2>&1
  echo "slide $N judge done rc=$? bytes=$(wc -c < "$O") $(date +%T)" >> _pool/b01_judge.log
}

echo "=== b01 judge start $(date +%F\ %T) ===" >> _pool/b01_judge.log
judge 001 qa/slide001/rejudge/r2/render-1.png qa/slide001/rejudge/r2/judge_attempt_1.txt &
sleep 15
judge 002 qa/slide002/rejudge/r2/render-1.png qa/slide002/rejudge/r2/judge_attempt_1.txt &
wait
echo "=== b01 judge end $(date +%F\ %T) ===" >> _pool/b01_judge.log
