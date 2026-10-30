#!/usr/bin/env bash
# b07 fresh comparison judges for slides 13,14 through the namespace vision gate.
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
SKILL=/home/codespace/ai_llm_slides/.agents/skills/image-analysis
cd "$NS"
PROMPT="$(cat judge_template.txt)"

judge() {
  local n="$1"
  local N
  N=$(printf '%03d' "$n")
  ./_pool/vision_gate.sh timeout 540 \
    python3 "$SKILL/scripts/analyze_image.py" comparison \
    "qa/slide${N}/b07/render-1.png" "unique_slides/slide_${N}.jpg" \
    --view "Slide $N recreation render vs original lecture frame" \
    --capture "13.33x7.5in slide, 150dpi render (2001x1125px) vs 960x540px original frame" \
    -p "$PROMPT" --timeout 420 --rounds 1 --tries 1 \
    > "qa/slide${N}/b07/judge_attempt_1.txt" 2>&1
  echo "slide $n judge rc=$? bytes=$(wc -c < qa/slide${N}/b07/judge_attempt_1.txt) $(date +%F\ %T)"
}

judge 13 &
sleep 15
judge 14 &
wait
echo "b07 judges done $(date +%F\ %T)"
