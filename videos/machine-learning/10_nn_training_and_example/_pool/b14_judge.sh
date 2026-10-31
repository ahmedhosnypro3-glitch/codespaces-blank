#!/usr/bin/env bash
# b14 judge dispatch: comparison judges for slides 27 and 28 through the gate.
# Frozen template verbatim; widened wall (W4 doctrine) since the gateway is slow.
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
SKILL=/home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py
cd "$NS"
PROMPT="$(cat judge_template.txt)"
ATTEMPT="${1:-1}"

run_one() {  # $1 = slide number
  local N="$1"
  local D="qa/slide${N}/b14"
  mkdir -p "$D"
  VISION_SLOTS=2 timeout 1200 bash "$NS/_pool/vision_gate.sh" \
    python3 "$SKILL" comparison "$D/render-1.png" "unique_slides/slide_${N}.jpg" \
    --view "Slide ${N} recreation render vs original lecture frame" \
    --capture "13.33x7.5in slide, 150dpi render (2000x1125px) vs 960x540px original frame" \
    -p "$PROMPT" --timeout 1100 --rounds 1 --tries 1 \
    > "$D/judge_attempt_${ATTEMPT}.txt" 2>&1
  echo "judge slide $N attempt $ATTEMPT rc=$? bytes=$(wc -c < "$D/judge_attempt_${ATTEMPT}.txt")"
}

run_one 27 &
sleep 15
run_one 28 &
wait
for N in 27 28; do
  grep -h 'FINAL VERDICT' "qa/slide${N}/b14/judge_attempt_${ATTEMPT}.txt" || echo "slide $N: NO VERDICT"
done
